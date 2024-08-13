#!/usr/bin/env python3
# Copyright (c) Meta Platforms, Inc. and affiliates.
# All rights reserved.
#
# This source code is licensed under the BSD-style license found in the
# LICENSE file in the root directory of this source tree.

# pyre-strict
# pyre-ignore-all-errors[56]

import contextlib
import enum
import functools
import logging
import math
import os
import uuid
from dataclasses import dataclass, field
from itertools import accumulate
from math import log2
from typing import Any, Callable, Dict, List, Optional, Tuple, Type, Union

import torch  # usort:skip
from torch import nn, Tensor  # usort:skip

import fbgemm_gpu.split_embedding_codegen_lookup_invokers as invokers

# from fbgemm_gpu.config import FeatureGateName
from fbgemm_gpu.runtime_monitor import (
    AsyncSeriesTimer,
    TBEStatsReporter,
    TBEStatsReporterConfig,
)
from fbgemm_gpu.split_embedding_configs import EmbOptimType as OptimType, SparseType
from fbgemm_gpu.split_table_batched_embeddings_ops_common import (
    BoundsCheckMode,
    CacheAlgorithm,
    CacheState,
    construct_cache_state,
    EmbeddingLocation,
    MAX_PREFETCH_DEPTH,
    MultiPassPrefetchConfig,
    PoolingMode,
    RecordCacheMetrics,
    SplitState,
)

try:
    if torch.version.hip:
        torch.ops.load_library(
            "//deeplearning/fbgemm/fbgemm_gpu/codegen:embedding_ops_hip_training"
        )
    else:
        torch.ops.load_library(
            "//deeplearning/fbgemm/fbgemm_gpu/codegen:embedding_ops_cuda_training"
        )
    torch.ops.load_library(
        "//deeplearning/fbgemm/fbgemm_gpu/codegen:embedding_ops_cpu_training"
    )
except Exception:
    pass


try:
    try:
        from torch.compiler import is_compiling

        def is_torchdynamo_compiling() -> bool:  # type: ignore[misc]
            # at least one test fails if we import is_compiling as a different name
            return is_compiling()

    except Exception:
        # torch.compiler.is_compiling is not available in torch 1.10
        from torch._dynamo import is_compiling as is_torchdynamo_compiling
except Exception:

    def is_torchdynamo_compiling() -> bool:  # type: ignore[misc]
        return False


DEFAULT_ASSOC = 32 if torch.version.hip is None else 64
INT8_EMB_ROW_DIM_OFFSET = 8


class DoesNotHavePrefix(Exception):
    pass


class ComputeDevice(enum.IntEnum):
    CPU = 0
    CUDA = 1
    MTIA = 2


class WeightDecayMode(enum.IntEnum):
    NONE = 0
    L2 = 1
    DECOUPLE = 2
    COUNTER = 3
    COWCLIP = 4
    DECOUPLE_GLOBAL = 5


class CounterWeightDecayMode(enum.IntEnum):
    NONE = 0
    L2 = 1
    DECOUPLE = 2


class LearningRateMode(enum.IntEnum):
    EQUAL = -1
    TAIL_ID_LR_INCREASE = 0
    TAIL_ID_LR_DECREASE = 1
    COUNTER_SGD = 2


class GradSumDecay(enum.IntEnum):
    NO_DECAY = -1
    CTR_DECAY = 0


@dataclass(frozen=True)
class TailIdThreshold:
    val: float = 0
    is_ratio: bool = False


@dataclass(frozen=True)
class CounterBasedRegularizationDefinition:
    counter_weight_decay_mode: CounterWeightDecayMode = CounterWeightDecayMode.NONE
    counter_halflife: int = -1
    adjustment_iter: int = -1
    adjustment_ub: float = 1.0
    learning_rate_mode: LearningRateMode = LearningRateMode.EQUAL
    grad_sum_decay: GradSumDecay = GradSumDecay.NO_DECAY
    tail_id_threshold: TailIdThreshold = field(default_factory=TailIdThreshold)
    max_counter_update_freq: int = 1000


@dataclass(frozen=True)
class CowClipDefinition:
    counter_weight_decay_mode: CounterWeightDecayMode = CounterWeightDecayMode.NONE
    counter_halflife: int = -1
    weight_norm_coefficient: float = 0.0
    lower_bound: float = 0.0


@dataclass(frozen=True)
class GlobalWeightDecayDefinition:
    start_iter: int = 0
    lower_bound: float = 0.0


# Keep in sync with fbgemm_gpu/include/fbgemm_gpu/split_embeddings_cache_cuda.cuh
class UVMCacheStatsIndex(enum.IntEnum):
    num_calls = 0
    num_requested_indices = 1
    num_unique_indices = 2
    num_unique_misses = 3
    num_conflict_unique_misses = 4
    num_conflict_misses = 5


def construct_split_state(
    embedding_specs: List[Tuple[int, int, EmbeddingLocation, ComputeDevice]],
    rowwise: bool,
    cacheable: bool,
    precision: SparseType = SparseType.FP32,
    int8_emb_row_dim_offset: int = INT8_EMB_ROW_DIM_OFFSET,
    placement: Optional[EmbeddingLocation] = None,
) -> SplitState:
    placements: List[EmbeddingLocation] = []
    offsets: List[int] = []
    dev_size: int = 0
    host_size: int = 0
    uvm_size: int = 0
    for num_embeddings, embedding_dim, location, _ in embedding_specs:
        assert (
            embedding_dim % 4 == 0
        ), f"embedding_dim must be a multiple of 4, but got {embedding_dim}"
        if precision == SparseType.INT8:
            embedding_dim += int8_emb_row_dim_offset
        state_size = num_embeddings * embedding_dim if not rowwise else num_embeddings
        location = placement if placement is not None else location
        if location == EmbeddingLocation.HOST:
            placements.append(EmbeddingLocation.HOST)
            offsets.append(host_size)
            host_size += state_size
        # If table is on device, then opimtizer is on device.
        # If table is managed, then if optimizer state is rowwise, optimizer is on device, otherwise optimizer is managed.
        elif location == EmbeddingLocation.DEVICE or rowwise:
            placements.append(EmbeddingLocation.DEVICE)
            offsets.append(dev_size)
            dev_size += state_size
        else:
            if cacheable and location == EmbeddingLocation.MANAGED_CACHING:
                placements.append(EmbeddingLocation.MANAGED_CACHING)
            else:
                placements.append(EmbeddingLocation.MANAGED)
            offsets.append(uvm_size)
            uvm_size += state_size
    assert len(placements) == len(offsets)
    return SplitState(
        dev_size=dev_size,
        host_size=host_size,
        uvm_size=uvm_size,
        placements=placements,
        offsets=offsets,
    )


def apply_split_helper(
    persistent_state_fn: Callable[[str, Tensor], None],
    set_attr_fn: Callable[
        [str, Union[Tensor, List[int], List[EmbeddingLocation]]], None
    ],
    current_device: torch.device,
    use_cpu: bool,
    feature_table_map: List[int],
    split: SplitState,
    prefix: str,
    dtype: Type[torch.dtype],
    enforce_hbm: bool = False,
    make_dev_param: bool = False,
    dev_reshape: Optional[Tuple[int, ...]] = None,
    uvm_tensors_log: Optional[List[str]] = None,
) -> None:
    set_attr_fn(f"{prefix}_physical_placements", split.placements)
    set_attr_fn(f"{prefix}_physical_offsets", split.offsets)

    offsets = [split.offsets[t] for t in feature_table_map]
    placements = [split.placements[t] for t in feature_table_map]
    persistent_state_fn(
        f"{prefix}_offsets",
        torch.tensor(offsets, device=current_device, dtype=torch.int64),
    )
    persistent_state_fn(
        f"{prefix}_placements",
        torch.tensor(placements, device=current_device, dtype=torch.int32),
    )
    if split.dev_size > 0:
        dev_buffer = torch.zeros(
            split.dev_size,
            device=current_device,
            # pyre-fixme[6]
            dtype=dtype,
        )
        dev_buffer = (
            dev_buffer.view(*dev_reshape) if dev_reshape is not None else dev_buffer
        )
    else:
        # pyre-fixme[6]
        dev_buffer = torch.empty(0, device=current_device, dtype=dtype)
    if make_dev_param:
        set_attr_fn(f"{prefix}_dev", nn.Parameter(dev_buffer))
    else:
        persistent_state_fn(f"{prefix}_dev", dev_buffer)
    if split.host_size > 0:
        if dtype == torch.uint8:
            persistent_state_fn(
                f"{prefix}_host",
                torch.zeros(
                    split.host_size,
                    device=current_device,
                    # pyre-fixme[6]: Expected `Optional[Type[torch._dtype]]` for
                    #  3rd param but got `Type[Type[torch._dtype]]`.
                    dtype=dtype,
                ),
            )
        else:
            set_attr_fn(
                f"{prefix}_host",
                nn.Parameter(
                    torch.zeros(
                        split.host_size,
                        device=current_device,
                        # pyre-fixme[6]: Expected `Optional[Type[torch._dtype]]`
                        #  for 3rd param but got `Type[Type[torch._dtype]]`.
                        dtype=dtype,
                    )
                ),
            )
        if uvm_tensors_log is not None:
            uvm_tensors_log.append(f"{prefix}_host")
    else:
        persistent_state_fn(
            f"{prefix}_host",
            # pyre-fixme[6]: For 3rd param expected `dtype` but got `Type[dtype]`.
            torch.empty(0, device=current_device, dtype=dtype),
        )
    if split.uvm_size > 0:
        assert not use_cpu
        if enforce_hbm:
            logging.info("Enforce hbm for the cache location")
            persistent_state_fn(
                f"{prefix}_uvm",
                torch.zeros(
                    split.uvm_size,
                    device=current_device,
                    # pyre-fixme[6]: Expected `Optional[Type[torch._dtype]]` for
                    #  3rd param but got `Type[Type[torch._dtype]]`.
                    dtype=dtype,
                ),
            )
        else:
            persistent_state_fn(
                f"{prefix}_uvm",
                torch.zeros(
                    split.uvm_size,
                    out=torch.ops.fbgemm.new_managed_tensor(
                        # pyre-fixme[6]: Expected `Optional[Type[torch._dtype]]`
                        #  for 3rd param but got `Type[Type[torch._dtype]]`.
                        torch.zeros(1, device=current_device, dtype=dtype),
                        [split.uvm_size],
                    ),
                ),
            )
            if uvm_tensors_log is not None:
                uvm_tensors_log.append(f"{prefix}_uvm")
    else:
        persistent_state_fn(
            f"{prefix}_uvm",
            # pyre-fixme[6]: For 3rd param expected `dtype` but got `Type[dtype]`.
            torch.empty(0, device=current_device, dtype=dtype),
        )


def generate_vbe_metadata(
    offsets: Tensor,
    batch_size_per_feature_per_rank: Optional[List[List[int]]],
    optimizer: OptimType,
    pooling_mode: PoolingMode,
    feature_dims_cpu: Tensor,
    device: torch.device,
) -> invokers.lookup_args.VBEMetadata:
    """
    Generate VBE metadata based on batch_size_per_feature_per_rank.
    Metadata includes:
        1) B_offsets - A tensor that contains batch size offsets for each
                        feature
        2) output_offsets_feature_rank - A tensor that contains output
                                            offsets for each feature
        3) B_offsets_per_rank_per_feature - A tensor that contains batch
                                            size offsets for each feature
                                            and rank
        4) max_B - The maximum batch size for all features
        5) max_B_feature_rank - The maximum batch size for all ranks and
                                features
        6) output_size - The output size (number of elements)
    """
    if batch_size_per_feature_per_rank is not None:
        assert (
            optimizer == OptimType.EXACT_ROWWISE_ADAGRAD
            or optimizer == OptimType.EXACT_SGD
            or optimizer == OptimType.NONE
        ), "Variable batch size TBE support is enabled for OptimType.EXACT_ROWWISE_ADAGRAD only"
        assert (
            pooling_mode != PoolingMode.NONE
        ), "Variable batch size TBE support is not enabled for PoolingMode.NONE"
        # TODO: Add input check
        zero_tensor = torch.zeros(1, device="cpu", dtype=torch.int32)

        # Create B offsets
        total_batch_size_per_feature = torch.tensor(
            batch_size_per_feature_per_rank, dtype=torch.int32, device="cpu"
        ).sum(dim=1)

        max_B = total_batch_size_per_feature.max().item()
        if not torch.jit.is_scripting() and is_torchdynamo_compiling():
            torch._check_is_size(max_B)
            torch._check(max_B < offsets.numel())

        Bs = torch.concat([zero_tensor, total_batch_size_per_feature])
        B_offsets = Bs.cumsum(dim=0).to(torch.int)

        # Create output offsets
        B_feature_rank = torch.tensor(
            batch_size_per_feature_per_rank,
            device="cpu",
            dtype=torch.int64,
        )
        max_B_feature_rank = B_feature_rank.max().item()
        if not torch.jit.is_scripting() and is_torchdynamo_compiling():
            torch._check_is_size(max_B_feature_rank)
            torch._check(max_B_feature_rank <= offsets.size(0))
        output_sizes_feature_rank = B_feature_rank.transpose(
            0, 1
        ) * feature_dims_cpu.view(1, -1)
        output_offsets_feature_rank = torch.concat(
            [
                zero_tensor.to(torch.int64),
                output_sizes_feature_rank.flatten().cumsum(dim=0),
            ]
        )
        output_size = output_offsets_feature_rank[-1].item()
        if not torch.jit.is_scripting() and is_torchdynamo_compiling():
            torch._check_is_size(output_size)

        # TODO: Support INT8 output
        # B_offsets_rank_per_feature is for rank and (b, t) mapping
        B_offsets_rank_per_feature = (
            torch.tensor(
                [
                    [0] + batch_size_per_feature
                    for batch_size_per_feature in batch_size_per_feature_per_rank
                ],
                device="cpu",
                dtype=torch.int32,
            )
            .cumsum(dim=1)
            .to(torch.int)
        )

        B_offsets = B_offsets.to(device, non_blocking=True)
        output_offsets_feature_rank = output_offsets_feature_rank.to(
            device, non_blocking=True
        )
        B_offsets_rank_per_feature = B_offsets_rank_per_feature.to(
            device, non_blocking=True
        )

        # TODO: Use int32 for B_offsets and int64 for output_offsets_feature_rank
        vbe_metadata = invokers.lookup_args.VBEMetadata(
            B_offsets=B_offsets,
            output_offsets_feature_rank=output_offsets_feature_rank,
            B_offsets_rank_per_feature=B_offsets_rank_per_feature,
            # pyre-ignore
            max_B=max_B,
            # pyre-ignore
            max_B_feature_rank=max_B_feature_rank,
            # pyre-ignore
            output_size=output_size,
        )
    else:
        vbe_metadata = invokers.lookup_args.VBEMetadata(
            B_offsets=None,
            output_offsets_feature_rank=None,
            B_offsets_rank_per_feature=None,
            max_B=-1,
            max_B_feature_rank=-1,
            output_size=-1,
        )
    return vbe_metadata


# pyre-fixme[13]: Attribute `uvm_cache_stats` is never initialized.
# pyre-fixme[13]: Attribute `local_uvm_cache_stats` is never initialized.
class SplitTableBatchedEmbeddingBagsCodegen(nn.Module):
    """
    Table Batched Embedding (TBE) operator.  Please see
    docs/table_batched_embedding_ops.py for the extended documentation.

    Multiple sparse features can share one embedding table.
    'feature_table_map' specifies the feature-table mapping.
    T:  number of logical tables
    T_: number of physical tables
    T >= T_

    For supported optimizer hyperparams, see inline comments below
    """

    embedding_specs: List[Tuple[int, int, EmbeddingLocation, ComputeDevice]]
    optimizer_args: invokers.lookup_args.OptimizerArgs
    lxu_cache_locations_list: List[Tensor]
    lxu_cache_locations_empty: Tensor
    timesteps_prefetched: List[int]
    record_cache_metrics: RecordCacheMetrics
    uvm_cache_stats: torch.Tensor
    local_uvm_cache_stats: torch.Tensor
    uuid: str
    last_uvm_cache_print_state: torch.Tensor
    _vbe_B_offsets: Optional[torch.Tensor]
    _vbe_max_B: int

    def __init__(  # noqa C901
        self,
        embedding_specs: List[
            Tuple[int, int, EmbeddingLocation, ComputeDevice]
        ],  # tuple of (rows, dims, placements, compute_devices)
        feature_table_map: Optional[List[int]] = None,  # [T]
        cache_algorithm: CacheAlgorithm = CacheAlgorithm.LRU,
        cache_load_factor: float = 0.2,
        cache_sets: int = 0,
        cache_reserved_memory: float = 0.0,
        cache_precision: SparseType = SparseType.FP32,
        weights_precision: SparseType = SparseType.FP32,
        output_dtype: SparseType = SparseType.FP32,
        enforce_hbm: bool = False,  # place all weights/momentums in HBM when using cache
        optimizer: OptimType = OptimType.EXACT_SGD,
        record_cache_metrics: Optional[RecordCacheMetrics] = None,
        gather_uvm_cache_stats: Optional[bool] = False,
        # General Optimizer args
        stochastic_rounding: bool = True,
        gradient_clipping: bool = False,
        max_gradient: float = 1.0,
        max_norm: float = 0.0,
        learning_rate: float = 0.01,
        # used by EXACT_ADAGRAD, EXACT_ROWWISE_ADAGRAD, LAMB, and ADAM only
        # NOTE that default is different from nn.optim.Adagrad default of 1e-10
        eps: float = 1.0e-8,
        momentum: float = 0.9,  # used by LARS-SGD
        # EXACT_ADAGRAD, SGD, EXACT_SGD do not support weight decay
        # LAMB, ADAM, PARTIAL_ROWWISE_ADAM, PARTIAL_ROWWISE_LAMB, LARS_SGD support decoupled weight decay
        # EXACT_ROWWISE_ADAGRAD support both L2 and decoupled weight decay (via weight_decay_mode)
        weight_decay: float = 0.0,
        weight_decay_mode: WeightDecayMode = WeightDecayMode.NONE,
        eta: float = 0.001,  # used by LARS-SGD,
        beta1: float = 0.9,  # used by LAMB and ADAM
        beta2: float = 0.999,  # used by LAMB and ADAM
        counter_based_regularization: Optional[
            CounterBasedRegularizationDefinition
        ] = None,  # used by Rowwise Adagrad
        cowclip_regularization: Optional[
            CowClipDefinition
        ] = None,  # used by Rowwise Adagrad
        pooling_mode: PoolingMode = PoolingMode.SUM,
        device: Optional[Union[str, int, torch.device]] = None,
        bounds_check_mode: BoundsCheckMode = BoundsCheckMode.WARNING,
        uvm_non_rowwise_momentum: bool = False,  # place non-rowwise momentum on UVM
        use_experimental_tbe: bool = False,  # set to True to use TBE v2 (only support NVIDIA GPUs)
        # set to True to enable prefetch pipeline, currently only supports LRU cache policy.
        # If a separate stream is used for prefetch, the optional forward_stream arg of prefetch function
        # should be set.
        prefetch_pipeline: bool = False,
        stats_reporter_config: Optional[TBEStatsReporterConfig] = None,
        # Embedding table names that are contained in this TBE.
        table_names: Optional[List[str]] = None,
        optimizer_state_dtypes: Optional[Dict[str, SparseType]] = None,
        multipass_prefetch_config: Optional[MultiPassPrefetchConfig] = None,
        # Global weight decay params
        global_weight_decay: Optional[GlobalWeightDecayDefinition] = None,
    ) -> None:
        super(SplitTableBatchedEmbeddingBagsCodegen, self).__init__()
        self.uuid = str(uuid.uuid4())
        self.logging_table_name: str = self.get_table_name_for_logging(table_names)
        self.pooling_mode = pooling_mode
        self.bounds_check_mode_int: int = bounds_check_mode.value
        self.weights_precision = weights_precision
        self.output_dtype: int = output_dtype.as_int()
        assert (
            not prefetch_pipeline or cache_algorithm == CacheAlgorithm.LRU
        ), "Only LRU cache policy supports prefetch_pipeline."
        self.prefetch_pipeline: bool = prefetch_pipeline
        self.lock_cache_line: bool = self.prefetch_pipeline
        self.use_uniq_cache_locations_bwd: bool = self.prefetch_pipeline
        self.multipass_prefetch_config: Optional[MultiPassPrefetchConfig] = (
            multipass_prefetch_config
        )

        if record_cache_metrics is not None:
            self.record_cache_metrics = record_cache_metrics
        else:
            self.record_cache_metrics = RecordCacheMetrics(False, False)

        if multipass_prefetch_config:
            assert (
                prefetch_pipeline
            ), "Multipass prefetch makes no sense in non-prefetch mode."
            assert (
                cache_algorithm == CacheAlgorithm.LRU
            ), "Multipass prefetch is only supported in LRU cache."
            assert (
                multipass_prefetch_config.num_passes > 0
            ), f"num_passes must be positive, get {multipass_prefetch_config.num_passes}"
            assert (
                multipass_prefetch_config.min_splitable_pass_size > 0
            ), f"min_splitable_pass_size must be positive, get {multipass_prefetch_config.min_splitable_pass_size}"
            assert (
                not self.record_cache_metrics.record_cache_miss_counter
                and not self.record_cache_metrics.record_tablewise_cache_miss
            ), "Unique cache miss counters are not accurate in multipass prefetch and therefore not supported"

        self.embedding_specs = embedding_specs
        (rows, dims, locations, compute_devices) = zip(*embedding_specs)
        T_ = len(self.embedding_specs)
        self.dims: List[int] = dims
        assert T_ > 0
        # mixed D is not supported by no bag kernels
        mixed_D = False
        D = self.dims[0]
        for d in self.dims:
            if d != D:
                mixed_D = True
                break
        if mixed_D:
            assert (
                self.pooling_mode != PoolingMode.NONE
            ), "Mixed dimension tables only supported for pooling tables."

        assert all(
            cd == compute_devices[0] for cd in compute_devices
        ), "Heterogenous compute_devices are NOT supported!"
        # Split TBE has different function schemas for CUDA and CPU.
        # For MTIA device type, it uses the CPU one.
        self.use_cpu: bool = (
            compute_devices[0] == ComputeDevice.CPU
            or compute_devices[0] == ComputeDevice.MTIA
        )

        assert not self.use_cpu or all(
            loc == EmbeddingLocation.HOST for loc in locations
        ), "ComputeDevice.CPU is only for EmbeddingLocation.HOST!"
        assert self.use_cpu or all(
            loc != EmbeddingLocation.HOST for loc in locations
        ), "EmbeddingLocation.HOST doesn't work for CUDA device!"
        if self.use_cpu or self.pooling_mode == PoolingMode.NONE:
            assert output_dtype in [
                SparseType.FP32,
                SparseType.FP16,
                SparseType.BF16,
            ], "Fused pooled embedding quantization only supported for cuda."

        if optimizer == OptimType.NONE:
            assert all(
                loc == EmbeddingLocation.DEVICE for loc in locations
            ), "OptimType.NONE supports only EmbeddingLocation.DEVICE"
            assert all(
                cd == ComputeDevice.CUDA for cd in compute_devices
            ), "OptimType.NONE supports only ComputeDevice.CUDA"
            assert (
                not mixed_D
            ), "OptimType.NONE does not support mixed embedding dimension"

        if device is None:
            self.current_device: torch.device = (
                torch.device("cpu")
                if self.use_cpu
                else torch.device(torch.cuda.current_device())
            )
        elif isinstance(device, torch.device):
            self.current_device = device
        else:
            self.current_device = torch.device(device)

        # add placeholder require_grad param tensor to enable autograd with int8 weights
        self.placeholder_autograd_tensor = nn.Parameter(
            torch.zeros(0, device=self.current_device, dtype=torch.float)
        )

        self.gather_uvm_cache_stats = gather_uvm_cache_stats
        # Define the size of uvm cache stats as class variable
        # to make it work with torch jit script.
        self.uvm_cache_stats_size = 6
        # 0: N_calls, 1: N_requested_indices, 2: N_unique_indices, 3: N_unique_misses,
        # 4: N_conflict_unique_misses, 5: N_conflict_misses

        # Reporter to collect runtime performance stats bottom-up. Reporter may
        # do aggregation across TBEs and publish results per training batch.
        # Example of stats include UVM cache hit rate, table I/O size, etc.
        self.stats_reporter: Optional[TBEStatsReporter] = (
            stats_reporter_config.create_reporter() if stats_reporter_config else None
        )
        self._uvm_tensors_log: List[str] = []

        self.bwd_wait_prefetch_timer: Optional[AsyncSeriesTimer] = None
        if self.stats_reporter:
            # When stats_reporter is present, we set up async series timer to
            # measure the GPU time per tracked event accordingly. Each of them
            # is attached to custom callback report function to report collected
            # duration with the corresponding event name.
            self.bwd_wait_prefetch_timer = AsyncSeriesTimer(
                functools.partial(
                    SplitTableBatchedEmbeddingBagsCodegen._report_wait_prefetch_time,
                    self,
                    event_name="bwd_wait_for_prefetch",
                )
            )

        self.int8_emb_row_dim_offset: int = INT8_EMB_ROW_DIM_OFFSET

        self.feature_table_map: List[int] = (
            feature_table_map if feature_table_map is not None else list(range(T_))
        )
        T = len(self.feature_table_map)
        assert T_ <= T
        table_has_feature = [False] * T_
        for t in self.feature_table_map:
            table_has_feature[t] = True
        assert all(table_has_feature), "Each table must have at least one feature!"

        feature_dims = [dims[t] for t in self.feature_table_map]
        D_offsets = [0] + list(accumulate(feature_dims))
        self.total_D: int = D_offsets[-1]
        self.max_D: int = max(dims)
        cached_dims = [
            embedding_spec[1]
            for embedding_spec in embedding_specs
            if embedding_spec[2] == EmbeddingLocation.MANAGED_CACHING
        ]
        self.max_D_cache: int = max(cached_dims) if len(cached_dims) > 0 else 0

        self.register_buffer(
            "D_offsets",
            torch.tensor(D_offsets, device=self.current_device, dtype=torch.int32),
        )
        hash_size_cumsum = [0] + list(accumulate(rows))
        self.total_hash_size: int = int(hash_size_cumsum[-1])
        if self.total_hash_size == 0:
            self.total_hash_size_bits: int = 0
        else:
            self.total_hash_size_bits: int = int(log2(float(self.total_hash_size)) + 1)
        # The last element is to easily access # of rows of each table by
        # hash_size_cumsum[t + 1] - hash_size_cumsum[t]
        hash_size_cumsum = [hash_size_cumsum[t] for t in self.feature_table_map] + [
            self.total_hash_size
        ]
        self.register_buffer(
            "hash_size_cumsum",
            torch.tensor(
                hash_size_cumsum, device=self.current_device, dtype=torch.int64
            ),
        )

        self.register_buffer(
            "rows_per_table",
            torch.tensor(
                [rows[t] for t in self.feature_table_map],
                device=self.current_device,
                dtype=torch.int64,
            ),
        )
        self.register_buffer(
            "bounds_check_warning",
            torch.tensor([0], device=self.current_device, dtype=torch.int64),
        )
        # Required for VBE
        self.register_buffer(
            "feature_dims",
            torch.tensor(feature_dims, device="cpu", dtype=torch.int64),
        )

        # A flag for indicating whether all embedding tables are placed in the
        # same locations
        self.use_homogeneous_placements: bool = all(
            loc == locations[0] for loc in locations
        )

        weight_split = construct_split_state(
            embedding_specs,
            rowwise=False,
            cacheable=True,
            precision=weights_precision,
        )
        table_embedding_dtype = weights_precision.as_dtype()

        self._apply_split(
            weight_split,
            prefix="weights",
            # pyre-fixme[6]: For 3rd param expected `Type[Type[_dtype]]` but got
            #  `Type[_dtype]`.
            dtype=table_embedding_dtype,
            enforce_hbm=enforce_hbm,
            make_dev_param=optimizer == OptimType.NONE,
            dev_reshape=(-1, self.max_D) if optimizer == OptimType.NONE else None,
        )

        assert optimizer not in (
            OptimType.SGD,
            OptimType.ROWWISE_ADAGRAD,
        ), f"Optimizer {optimizer} is deprecated in the CPU + GPU modes."

        if self.use_cpu:
            # Construct optimizer states
            assert optimizer in (
                OptimType.EXACT_ADAGRAD,
                OptimType.EXACT_ROWWISE_ADAGRAD,
                OptimType.EXACT_SGD,
            ), f"Optimizer {optimizer} is not supported in CPU mode."
        else:
            assert optimizer in (
                OptimType.ADAM,
                OptimType.EXACT_ADAGRAD,
                OptimType.EXACT_ROWWISE_ADAGRAD,
                OptimType.EXACT_SGD,
                OptimType.LAMB,
                OptimType.LARS_SGD,
                OptimType.PARTIAL_ROWWISE_ADAM,
                OptimType.PARTIAL_ROWWISE_LAMB,
                OptimType.NONE,
            ), f"Optimizer {optimizer} is not supported."

        self.stochastic_rounding = stochastic_rounding
        self.optimizer = optimizer

        self.weight_decay_mode = weight_decay_mode
        if (weight_decay_mode == WeightDecayMode.COUNTER) != (
            counter_based_regularization is not None
        ):
            raise AssertionError(
                "Need to set weight_decay_mode=WeightDecayMode.COUNTER together with valid counter_based_regularization"
            )
        if (weight_decay_mode == WeightDecayMode.COWCLIP) != (
            cowclip_regularization is not None
        ):
            raise AssertionError(
                "Need to set weight_decay_mode=WeightDecayMode.COWCLIP together with valid cowclip_regularization"
            )

        self._used_rowwise_adagrad_with_counter: bool = (
            optimizer == OptimType.EXACT_ROWWISE_ADAGRAD
            and (
                weight_decay_mode in (WeightDecayMode.COUNTER, WeightDecayMode.COWCLIP)
            )
        )

        if weight_decay_mode == WeightDecayMode.DECOUPLE_GLOBAL and (
            not optimizer == OptimType.EXACT_ROWWISE_ADAGRAD
            or global_weight_decay is None
        ):
            raise AssertionError(
                """weight_decay_mode=WeightDecayMode.DECOUPLE_GLOBAL is supported for
                optimizer=OptimType.EXACT_ROWWISE_ADAGRAD and global_weight_decay cannot be None.
                """
            )

        self._used_rowwise_adagrad_with_global_weight_decay: bool = (
            optimizer == OptimType.EXACT_ROWWISE_ADAGRAD
            and (weight_decay_mode == WeightDecayMode.DECOUPLE_GLOBAL)
        )
        logging.info(
            f"Using global weight decay = {self._used_rowwise_adagrad_with_global_weight_decay}"
        )
        # Declare GWD params here to avoid torch.jit.script error
        if global_weight_decay is None:
            global_weight_decay = GlobalWeightDecayDefinition()

        self.gwd_start_iter: int = global_weight_decay.start_iter
        self.gwd_lower_bound: float = global_weight_decay.lower_bound

        if counter_based_regularization is None:
            counter_based_regularization = CounterBasedRegularizationDefinition()
        if cowclip_regularization is None:
            cowclip_regularization = CowClipDefinition()
        self._max_counter_update_freq: int = -1
        # Extract parameters from CounterBasedRegularizationDefinition or CowClipDefinition
        # which are passed as entries for OptimizerArgs
        if self._used_rowwise_adagrad_with_counter:
            if self.weight_decay_mode == WeightDecayMode.COUNTER:
                self._max_counter_update_freq = (
                    counter_based_regularization.max_counter_update_freq
                )
                opt_arg_weight_decay_mode = (
                    counter_based_regularization.counter_weight_decay_mode
                )
                counter_halflife = counter_based_regularization.counter_halflife
            else:
                opt_arg_weight_decay_mode = (
                    cowclip_regularization.counter_weight_decay_mode
                )
                counter_halflife = cowclip_regularization.counter_halflife
        else:
            opt_arg_weight_decay_mode = weight_decay_mode
            # Default: -1, no decay applied, as a placeholder for OptimizerArgs
            # which should not be effective when CounterBasedRegularizationDefinition
            # and CowClipDefinition are not used
            counter_halflife = -1

        self.optimizer_args = invokers.lookup_args.OptimizerArgs(
            stochastic_rounding=stochastic_rounding,
            gradient_clipping=gradient_clipping,
            max_gradient=max_gradient,
            max_norm=max_norm,
            learning_rate=learning_rate,
            eps=eps,
            beta1=beta1,
            beta2=beta2,
            weight_decay=weight_decay,
            weight_decay_mode=opt_arg_weight_decay_mode.value,
            eta=eta,
            momentum=momentum,
            counter_halflife=counter_halflife,
            adjustment_iter=counter_based_regularization.adjustment_iter,
            adjustment_ub=counter_based_regularization.adjustment_ub,
            learning_rate_mode=counter_based_regularization.learning_rate_mode.value,
            grad_sum_decay=counter_based_regularization.grad_sum_decay.value,
            tail_id_threshold=counter_based_regularization.tail_id_threshold.val,
            is_tail_id_thresh_ratio=int(
                counter_based_regularization.tail_id_threshold.is_ratio
            ),
            total_hash_size=self.total_hash_size,
            weight_norm_coefficient=cowclip_regularization.weight_norm_coefficient,
            lower_bound=cowclip_regularization.lower_bound,
            regularization_mode=weight_decay_mode.value,
        )

        if optimizer != OptimType.NONE:
            assert (
                optimizer == OptimType.PARTIAL_ROWWISE_ADAM
                or optimizer_state_dtypes is None
            ), "optimizer_state_dtypes option is only supported for OptimType.PARTIAL_ROWWISE_ADAM"
            if optimizer in (OptimType.EXACT_SGD,):
                # NOTE: make TorchScript work!
                self._register_nonpersistent_buffers("momentum1")
            else:
                momentum1_dtype = (
                    torch.float32
                    if (
                        optimizer_state_dtypes is None
                        or "momentum1" not in optimizer_state_dtypes
                    )
                    else optimizer_state_dtypes["momentum1"].as_dtype()
                )
                rowwise = optimizer in [
                    OptimType.EXACT_ROWWISE_ADAGRAD,
                ]
                self._apply_split(
                    construct_split_state(
                        embedding_specs,
                        rowwise=rowwise,
                        cacheable=False,
                        placement=(
                            EmbeddingLocation.MANAGED
                            if ((not rowwise) and uvm_non_rowwise_momentum)
                            else None
                        ),
                    ),
                    prefix="momentum1",
                    # pyre-fixme[6]: Expected `Type[Type[torch._dtype]]` for 3rd param
                    #  but got `Type[torch.float32]`.
                    dtype=momentum1_dtype,
                    enforce_hbm=enforce_hbm,
                )
            if optimizer in (
                OptimType.ADAM,
                OptimType.PARTIAL_ROWWISE_ADAM,
                OptimType.LAMB,
                OptimType.PARTIAL_ROWWISE_LAMB,
            ):
                rowwise = optimizer in (
                    OptimType.PARTIAL_ROWWISE_ADAM,
                    OptimType.PARTIAL_ROWWISE_LAMB,
                )
                momentum2_dtype = (
                    torch.float32
                    if (
                        optimizer_state_dtypes is None
                        or "momentum2" not in optimizer_state_dtypes
                    )
                    else optimizer_state_dtypes["momentum2"].as_dtype()
                )
                self._apply_split(
                    construct_split_state(
                        embedding_specs,
                        rowwise=rowwise,
                        cacheable=False,
                        placement=(
                            EmbeddingLocation.MANAGED
                            if ((not rowwise) and uvm_non_rowwise_momentum)
                            else None
                        ),
                    ),
                    prefix="momentum2",
                    # pyre-fixme[6]: Expected `Type[Type[torch._dtype]]` for 3rd param
                    #  but got `Type[torch.float32]`.
                    dtype=momentum2_dtype,
                )
            else:
                # NOTE: make TorchScript work!
                self._register_nonpersistent_buffers("momentum2")
            if self._used_rowwise_adagrad_with_counter:
                self._apply_split(
                    construct_split_state(
                        embedding_specs,
                        rowwise=True,
                        cacheable=False,
                    ),
                    prefix="prev_iter",
                    # TODO: ideally we should use int64 to track iter but it failed to compile.
                    # It may be related to low precision training code. Currently using float32
                    # as a workaround while investigating the issue.
                    # pyre-fixme[6]: Expected `Type[Type[torch._dtype]]` for 3rd param
                    #  but got `Type[torch.float32]`.
                    dtype=torch.float32,
                )
                self._apply_split(
                    construct_split_state(
                        embedding_specs,
                        rowwise=True,
                        cacheable=False,
                    ),
                    prefix="row_counter",
                    # pyre-fixme[6]: Expected `Type[Type[torch._dtype]]` for 3rd param
                    #  but got `Type[torch.float32]`.
                    dtype=torch.float32,
                )
                self.register_buffer(
                    "max_counter", torch.tensor([1], dtype=torch.float32)
                )
            elif self._used_rowwise_adagrad_with_global_weight_decay:
                self._apply_split(
                    construct_split_state(
                        embedding_specs,
                        rowwise=True,
                        cacheable=False,
                    ),
                    prefix="prev_iter",
                    # TODO: ideally we should use int64 to track iter but it failed to compile.
                    # It may be related to low precision training code. Currently using float32
                    # as a workaround while investigating the issue.
                    # pyre-fixme[6]: Expected `Type[Type[torch._dtype]]` for 3rd param
                    #  but got `Type[torch.float32]`.
                    dtype=torch.float32,
                )
                self._register_nonpersistent_buffers("row_counter")
                self.register_buffer(
                    "max_counter",
                    torch.ones(1, dtype=torch.float32, device=self.current_device),
                    persistent=False,
                )
            else:
                self._register_nonpersistent_buffers("prev_iter")
                self._register_nonpersistent_buffers("row_counter")
                self.register_buffer(
                    "max_counter",
                    torch.ones(1, dtype=torch.float32, device=self.current_device),
                    persistent=False,
                )
            if (
                optimizer
                in (
                    OptimType.ADAM,
                    OptimType.LAMB,
                    OptimType.PARTIAL_ROWWISE_ADAM,
                    OptimType.PARTIAL_ROWWISE_LAMB,
                )
                or self._used_rowwise_adagrad_with_global_weight_decay
            ):
                self.register_buffer(
                    "iter",
                    torch.zeros(1, dtype=torch.int64, device=self.current_device),
                )

            else:
                self.register_buffer(
                    "iter",
                    torch.zeros(1, dtype=torch.int64, device=self.current_device),
                    persistent=False,
                )

        cache_state = construct_cache_state(rows, locations, self.feature_table_map)

        # Add table-wise cache miss counter
        if self.record_cache_metrics.record_tablewise_cache_miss:
            num_tables = len(cache_state.cache_hash_size_cumsum) - 1
            self.register_buffer(
                "table_wise_cache_miss",
                torch.zeros(
                    num_tables,
                    device=self.current_device,
                    dtype=torch.int64,
                ),
            )
        # NOTE: make TorchScript work!
        else:
            self.register_buffer(
                "table_wise_cache_miss",
                torch.zeros(
                    0,
                    device=self.current_device,
                    dtype=torch.int64,
                ),
            )

        if cache_precision == SparseType.FP32:
            cache_embedding_dtype = torch.float32
        elif cache_precision == SparseType.FP16:
            cache_embedding_dtype = torch.float16
        else:
            raise AssertionError(f"cache_precision {cache_precision} not supported!")

        self._apply_cache_state(
            cache_state,
            cache_algorithm,
            cache_load_factor,
            cache_sets,
            cache_reserved_memory,
            dtype=cache_embedding_dtype,
        )

        self.log(f"Contents: {table_names}")
        self.log(
            f"Using fused {optimizer} with optimizer_args={self.optimizer_args if optimizer != OptimType.NONE else None}"
        )
        self.log(
            f"Using rowwise_adagrad_with_counter={self._used_rowwise_adagrad_with_counter}"
        )

        self.step = 0
        self.last_reported_step = 0
        self.last_reported_uvm_stats: List[float] = []

        # Check whether to use TBE v2
        is_experimental = False
        if use_experimental_tbe:
            is_experimental = True
            self.log("use_experimental_tbe is set to True; Using experimental TBE")

        elif int(os.environ.get("FBGEMM_EXPERIMENTAL_TBE", "0")) == 1:
            # Keep the old feature enablement mechanism to ensure no negative impact on models that have already adopted TBE v2
            is_experimental = True
            self.log("FBGEMM_EXPERIMENTAL_TBE is set to True; Using experimental TBE")

        # NOTE: Keep this disabled for now until the backend lands into Pyper
        # elif FeatureGateName.TBE_V2.is_enabled():
        #     is_experimental = True
        #     self.log("TBE_V2 Knob is set to True; Using experimental TBE")

        self.is_experimental: bool = is_experimental

    @torch.jit.ignore
    def log(self, msg: str) -> None:
        """Log with TBE id prefix to distinguish between multiple TBE instances per process."""
        logging.info(f"[TBE={self.uuid}] {msg}")

    def _register_nonpersistent_buffers(self, prefix: str) -> None:
        # NOTE: make TorchScript work!
        self.register_buffer(
            f"{prefix}_dev",
            torch.zeros(1, dtype=torch.int64, device=self.current_device),
            persistent=False,
        )
        self.register_buffer(
            f"{prefix}_host",
            torch.zeros(1, dtype=torch.int64, device=self.current_device),
            persistent=False,
        )
        self.register_buffer(
            f"{prefix}_uvm",
            torch.zeros(1, dtype=torch.int64, device=self.current_device),
            persistent=False,
        )
        self.register_buffer(
            f"{prefix}_placements",
            torch.zeros(1, dtype=torch.int64, device=self.current_device),
            persistent=False,
        )
        self.register_buffer(
            f"{prefix}_offsets",
            torch.zeros(1, dtype=torch.int64, device=self.current_device),
            persistent=False,
        )

    @staticmethod
    def get_table_name_for_logging(table_names: Optional[List[str]]) -> str:
        """
        Given list of all table names in the TBE, generate a string to represent
        them in logging. If there's more than one table, this method will count
        them than list them.
        """
        if table_names is None:
            return "<Unknown>"
        # Do this because sometimes multiple shards of the same table could appear
        # in one TBE.
        table_name_set = set(table_names)
        if len(table_name_set) == 1:
            return next(iter(table_name_set))
        return f"<{len(table_name_set)} tables>"

    @staticmethod
    def get_prefetch_passes(
        multipass_prefetch_config: Optional[MultiPassPrefetchConfig],
        input_tensor: Tensor,
        output_tensor: Tensor,
    ) -> List[Tuple[Tensor, Tensor, int]]:
        """
        Given input (the indices to forward), return the segmentation for each pass
        in the format of (input[start_idx:end_idx], output[start_idx:end_idx], start_idx).

        Caller should guarantee input and output are having the size on dimension 0
        The returned segments are guaranteed to completely and non-overlappingly cover the input tensor.

        In non-multipass-prefetch mode, it returns the input/output tensor itself.
        """
        if multipass_prefetch_config is None:
            return [(input_tensor, output_tensor, 0)]
        mpp_config: MultiPassPrefetchConfig = multipass_prefetch_config

        N = input_tensor.size(0)
        if N <= mpp_config.num_passes or mpp_config.num_passes == 1:
            # One row per pass, just don't split
            return [(input_tensor, output_tensor, 0)]

        pass_size: int = max(
            (N + mpp_config.num_passes - 1) // mpp_config.num_passes,
            mpp_config.min_splitable_pass_size,
        )

        return list(
            zip(
                torch.split(input_tensor, pass_size),
                torch.split(output_tensor, pass_size),
                range(0, N, pass_size),
            )
        )

    def get_states(self, prefix: str) -> Tuple[Tensor, Tensor, Tensor, Tensor, Tensor]:
        if not hasattr(self, f"{prefix}_physical_placements"):
            raise DoesNotHavePrefix()
        dev_param = getattr(self, f"{prefix}_dev")
        host_param = getattr(self, f"{prefix}_host")
        uvm_param = getattr(self, f"{prefix}_uvm")
        placements = getattr(self, f"{prefix}_physical_placements")
        offsets = getattr(self, f"{prefix}_physical_offsets")
        return (
            dev_param,
            host_param,
            uvm_param,
            torch.tensor(placements, dtype=torch.int32),
            torch.tensor(offsets, dtype=torch.int64),
        )

    def get_all_states(self) -> List[Tuple[Tensor, Tensor, Tensor, Tensor, Tensor]]:
        all_states = []
        for prefix in ["weights", "momentum1", "momentum2", "prev_iter", "row_counter"]:
            try:
                all_states.append(self.get_states(prefix))
            except DoesNotHavePrefix:
                pass
        return all_states

    @torch.jit.export
    def get_cache_miss_counter(self) -> Tensor:
        # cache_miss_counter contains two items:
        # The first one is cache_miss_forward_count which records the total number of forwards which has at least one cache miss
        # The second one is the unique_cache_miss_count which records to total number of unique (dedup) cache misses

        return self.cache_miss_counter

    @torch.jit.export
    def get_table_wise_cache_miss(self) -> Tensor:
        # table_wise_cache_miss contains all the cache miss count for each table in this embedding table object:

        return self.table_wise_cache_miss

    # The callback function for AsyncTimer to record duration to different event
    def _report_wait_prefetch_time(
        self,
        it_step: int,
        dur_ms: float,
        event_name: str,
    ) -> None:
        assert (
            self.stats_reporter
        ), "We should not be here. AsyncTimer only happens with reporter present."
        self.stats_reporter.report_duration(
            iteration_step=it_step,
            event_name=event_name,
            duration_ms=dur_ms,
            embedding_id=self.logging_table_name,
            tbe_id=self.uuid,
        )

    @torch.jit.ignore
    def _report_tbe_mem_usage(
        self,
    ) -> None:
        if self.stats_reporter is None:
            return

        stats_reporter: TBEStatsReporter = self.stats_reporter
        if not stats_reporter.should_report(self.step):
            return

        total_mem_usage = sum(
            param.numel() * param.element_size() for param in self.parameters()
        ) + sum(buffer.numel() * buffer.element_size() for buffer in self.buffers())
        if self.use_cpu:
            total_hbm_usage = 0
            total_uvm_usage = total_mem_usage
        else:
            # hbm usage is total usage minus uvm usage
            total_uvm_usage = sum(
                getattr(self, tensor_name).numel()
                * getattr(self, tensor_name).element_size()
                for tensor_name in self._uvm_tensors_log
                if hasattr(self, tensor_name)
            )
            total_hbm_usage = total_mem_usage - total_uvm_usage

        stats_reporter.report_data_amount(
            iteration_step=self.step,
            event_name="tbe.total_hbm_usage",
            data_bytes=total_hbm_usage,
            embedding_id=self.logging_table_name,
            tbe_id=self.uuid,
        )
        stats_reporter.report_data_amount(
            iteration_step=self.step,
            event_name="tbe.total_uvm_usage",
            data_bytes=total_uvm_usage,
            embedding_id=self.logging_table_name,
            tbe_id=self.uuid,
        )

    @torch.jit.ignore
    def _report_io_size_count(self, event: str, data: Tensor) -> Tensor:
        if self.stats_reporter is None:
            return data
        stats_reporter: TBEStatsReporter = self.stats_reporter
        if stats_reporter.should_report(self.step):
            stats_reporter.report_data_amount(
                iteration_step=self.step,
                event_name=f"tbe.{event}_size",
                data_bytes=data.element_size() * data.numel(),
                embedding_id=self.logging_table_name,
                tbe_id=self.uuid,
            )
            stats_reporter.report_data_amount(
                iteration_step=self.step,
                event_name=f"tbe.{event}_count",
                data_bytes=data.numel(),
                embedding_id=self.logging_table_name,
                tbe_id=self.uuid,
            )
        return data

    @torch.jit.ignore
    def _generate_vbe_metadata(
        self,
        offsets: Tensor,
        batch_size_per_feature_per_rank: Optional[List[List[int]]],
    ) -> invokers.lookup_args.VBEMetadata:
        # Blocking D2H copy, but only runs at first call
        self.feature_dims = self.feature_dims.cpu()
        return generate_vbe_metadata(
            offsets,
            batch_size_per_feature_per_rank,
            self.optimizer,
            self.pooling_mode,
            self.feature_dims,
            self.current_device,
        )

    def forward(  # noqa: C901
        self,
        indices: Tensor,
        offsets: Tensor,
        per_sample_weights: Optional[Tensor] = None,
        feature_requires_grad: Optional[Tensor] = None,
        # 2D tensor of batch size for each rank and feature.
        # Shape (number of features, number of ranks)
        batch_size_per_feature_per_rank: Optional[List[List[int]]] = None,
        total_unique_indices: Optional[int] = None,
    ) -> Tensor:
        # Generate VBE metadata
        vbe_metadata = self._generate_vbe_metadata(
            offsets, batch_size_per_feature_per_rank
        )

        (indices, offsets) = indices.long(), offsets.long()
        # Force casting per_sample_weights to float
        if per_sample_weights is not None:
            per_sample_weights = per_sample_weights.float()

        if self.bounds_check_mode_int != BoundsCheckMode.NONE.value:
            torch.ops.fbgemm.bounds_check_indices(
                self.rows_per_table,
                indices,
                offsets,
                self.bounds_check_mode_int,
                self.bounds_check_warning,
                per_sample_weights,
                B_offsets=vbe_metadata.B_offsets,
                max_B=vbe_metadata.max_B,
            )

        if not is_torchdynamo_compiling():
            # Mutations of nn.Module attr forces dynamo restart of Analysis which increases compilation time

            # Storing tensors for linear_cache_indices recomputation
            self._indices = indices
            self._offsets = offsets
            self._vbe_B_offsets = vbe_metadata.B_offsets
            self._vbe_max_B = vbe_metadata.max_B

            self.step += 1
            self._report_io_size_count("fwd_input", indices)
            self._report_tbe_mem_usage()

        if len(self.timesteps_prefetched) == 0:
            # In forward, we don't enable multi-pass prefetch as we want the process
            # to be as fast as possible and memory usage doesn't matter (will be recycled
            # by dense fwd/bwd)
            self._prefetch(
                indices, offsets, vbe_metadata, multipass_prefetch_config=None
            )

        if len(self.timesteps_prefetched) > 0:
            self.timesteps_prefetched.pop(0)

        self.lxu_cache_locations = (
            self.lxu_cache_locations_empty
            if len(self.lxu_cache_locations_list) == 0
            else self.lxu_cache_locations_list.pop(0)
        )
        common_args = invokers.lookup_args.CommonArgs(
            placeholder_autograd_tensor=self.placeholder_autograd_tensor,
            dev_weights=self.weights_dev,
            host_weights=self.weights_host,
            uvm_weights=self.weights_uvm,
            lxu_cache_weights=self.lxu_cache_weights,
            weights_placements=self.weights_placements,
            weights_offsets=self.weights_offsets,
            D_offsets=self.D_offsets,
            total_D=self.total_D,
            max_D=self.max_D,
            hash_size_cumsum=self.hash_size_cumsum,
            total_hash_size_bits=self.total_hash_size_bits,
            indices=indices,
            offsets=offsets,
            pooling_mode=self.pooling_mode,
            indice_weights=per_sample_weights,
            feature_requires_grad=feature_requires_grad,
            lxu_cache_locations=self.lxu_cache_locations,
            # Pass the local_uvm_cache_stats bc only that information is
            # relevant for the current iteration
            uvm_cache_stats=(
                self.local_uvm_cache_stats
                if (
                    self.gather_uvm_cache_stats
                    # Unique conflict misses are only collected when using CacheAlgorithm.LRU
                    and self.cache_algorithm == CacheAlgorithm.LRU
                )
                else None
            ),
            output_dtype=self.output_dtype,
            vbe_metadata=vbe_metadata,
            is_experimental=self.is_experimental,
            use_uniq_cache_locations_bwd=self.use_uniq_cache_locations_bwd,
            use_homogeneous_placements=self.use_homogeneous_placements,
        )

        if self.optimizer == OptimType.NONE:
            assert (
                total_unique_indices is not None
                and total_unique_indices <= indices.numel()
            ), f"OptimType.NONE requires total_unique_indices. Please pass it or check the value (total_unique_indices = {total_unique_indices})"
            return self._report_io_size_count(
                "fwd_output",
                invokers.lookup_none.invoke(
                    common_args, self.optimizer_args, total_unique_indices
                ),
            )
        elif self.optimizer == OptimType.EXACT_SGD:
            return self._report_io_size_count(
                "fwd_output",
                invokers.lookup_sgd.invoke(common_args, self.optimizer_args),
            )

        momentum1 = invokers.lookup_args.Momentum(
            dev=self.momentum1_dev,
            host=self.momentum1_host,
            uvm=self.momentum1_uvm,
            offsets=self.momentum1_offsets,
            placements=self.momentum1_placements,
        )

        if self.optimizer == OptimType.LARS_SGD:
            return self._report_io_size_count(
                "fwd_output",
                invokers.lookup_lars_sgd.invoke(
                    common_args, self.optimizer_args, momentum1
                ),
            )
        if self.optimizer == OptimType.EXACT_ADAGRAD:
            return self._report_io_size_count(
                "fwd_output",
                invokers.lookup_adagrad.invoke(
                    common_args, self.optimizer_args, momentum1
                ),
            )

        momentum2 = invokers.lookup_args.Momentum(
            dev=self.momentum2_dev,
            host=self.momentum2_host,
            uvm=self.momentum2_uvm,
            offsets=self.momentum2_offsets,
            placements=self.momentum2_placements,
        )
        # Ensure iter is always on CPU so the increment doesn't synchronize.
        if not self.iter.is_cpu:
            self.iter = self.iter.cpu()
        self.iter[0] += 1

        if self.optimizer == OptimType.ADAM:
            return self._report_io_size_count(
                "fwd_output",
                invokers.lookup_adam.invoke(
                    common_args,
                    self.optimizer_args,
                    momentum1,
                    momentum2,
                    # pyre-fixme[6]: Expected `int` for 5th param but got `Union[float,
                    #  int]`.
                    self.iter.item(),
                ),
            )
        if self.optimizer == OptimType.PARTIAL_ROWWISE_ADAM:
            return self._report_io_size_count(
                "fwd_output",
                invokers.lookup_partial_rowwise_adam.invoke(
                    common_args,
                    self.optimizer_args,
                    momentum1,
                    momentum2,
                    # pyre-fixme[6]: Expected `int` for 5th param but got `Union[float,
                    #  int]`.
                    self.iter.item(),
                ),
            )
        if self.optimizer == OptimType.LAMB:
            return self._report_io_size_count(
                "fwd_output",
                invokers.lookup_lamb.invoke(
                    common_args,
                    self.optimizer_args,
                    momentum1,
                    momentum2,
                    # pyre-fixme[6]: Expected `int` for 5th param but got `Union[float,
                    #  int]`.
                    self.iter.item(),
                ),
            )
        if self.optimizer == OptimType.PARTIAL_ROWWISE_LAMB:
            return self._report_io_size_count(
                "fwd_output",
                invokers.lookup_partial_rowwise_lamb.invoke(
                    common_args,
                    self.optimizer_args,
                    momentum1,
                    momentum2,
                    # pyre-fixme[6]: Expected `int` for 5th param but got `Union[float,
                    #  int]`.
                    self.iter.item(),
                ),
            )

        prev_iter = invokers.lookup_args.Momentum(
            dev=self.prev_iter_dev,
            host=self.prev_iter_host,
            uvm=self.prev_iter_uvm,
            offsets=self.prev_iter_offsets,
            placements=self.prev_iter_placements,
        )
        row_counter = invokers.lookup_args.Momentum(
            dev=self.row_counter_dev,
            host=self.row_counter_host,
            uvm=self.row_counter_uvm,
            offsets=self.row_counter_offsets,
            placements=self.row_counter_placements,
        )
        if self._used_rowwise_adagrad_with_counter:
            if (
                self._max_counter_update_freq > 0
                and self.iter.item() % self._max_counter_update_freq == 0
            ):
                row_counter_dev = self.row_counter_dev.detach()
                if row_counter_dev.numel() > 0:
                    self.max_counter[0] = torch.max(row_counter_dev).cpu().item() + 1
                else:
                    self.max_counter[0] = 1

        if self.optimizer == OptimType.EXACT_ROWWISE_ADAGRAD:
            if self._used_rowwise_adagrad_with_counter:
                return self._report_io_size_count(
                    "fwd_output",
                    invokers.lookup_rowwise_adagrad_with_counter.invoke(
                        common_args,
                        self.optimizer_args,
                        momentum1,
                        prev_iter,
                        row_counter,
                        int(
                            self.iter.item()
                        ),  # Cast to int to suppress pyre type error
                        self.max_counter.item(),
                    ),
                )
            elif self._used_rowwise_adagrad_with_global_weight_decay:
                apply_global_weight_decay = (
                    self.step >= self.gwd_start_iter and self.training
                )
                return self._report_io_size_count(
                    "fwd_output",
                    invokers.lookup_rowwise_adagrad.invoke(
                        common_args,
                        self.optimizer_args,
                        momentum1,
                        iter=int(self.iter.item()),
                        apply_global_weight_decay=apply_global_weight_decay,
                        prev_iter_dev=self.prev_iter_dev,
                        gwd_lower_bound=self.gwd_lower_bound,
                    ),
                )
            else:
                return self._report_io_size_count(
                    "fwd_output",
                    invokers.lookup_rowwise_adagrad.invoke(
                        common_args,
                        self.optimizer_args,
                        momentum1,
                    ),
                )

        raise ValueError(f"Invalid OptimType: {self.optimizer}")

    def reset_uvm_cache_stats(self) -> None:
        assert (
            self.gather_uvm_cache_stats
        ), "gather_uvm_cache_stats should be set to true to access uvm cache stats."
        self.uvm_cache_stats.zero_()
        self.local_uvm_cache_stats.zero_()

    def get_uvm_cache_stats(self, use_local_cache: bool = False) -> Tensor:
        assert (
            self.gather_uvm_cache_stats
        ), "gather_uvm_cache_stats should be set to true to access uvm cache stats."
        return self.local_uvm_cache_stats if use_local_cache else self.uvm_cache_stats

    def _get_uvm_cache_print_state(self, use_local_cache: bool = False) -> List[float]:
        snapshot = self.get_uvm_cache_stats(use_local_cache)
        if use_local_cache:
            return snapshot.tolist()

        # Stats are accumulated over multiple steps.  Compute delta, and update state.
        delta = snapshot - self.last_uvm_cache_print_state
        self.last_uvm_cache_print_state = snapshot.clone()
        return delta.tolist()

    @torch.jit.ignore
    def print_uvm_cache_stats(self, use_local_cache: bool = False) -> None:
        # TODO: Create a separate reporter class to unify the stdlog reporting
        uvm_cache_stats: List[float] = self._get_uvm_cache_print_state(use_local_cache)
        N = max(1, uvm_cache_stats[0])
        m = {
            "N_called": uvm_cache_stats[UVMCacheStatsIndex.num_calls],
            "requested_indices": uvm_cache_stats[
                UVMCacheStatsIndex.num_requested_indices
            ]
            / N,
            "unique_indices": uvm_cache_stats[UVMCacheStatsIndex.num_unique_indices]
            / N,
            "unique_misses": uvm_cache_stats[UVMCacheStatsIndex.num_unique_misses] / N,
            "conflict_unique_misses": uvm_cache_stats[
                UVMCacheStatsIndex.num_conflict_unique_misses
            ]
            / N,
            "conflict_misses": uvm_cache_stats[UVMCacheStatsIndex.num_conflict_misses]
            / N,
        }
        if uvm_cache_stats[1]:
            m.update(
                {
                    "unique indices / requested indices": uvm_cache_stats[
                        UVMCacheStatsIndex.num_unique_indices
                    ]
                    / uvm_cache_stats[UVMCacheStatsIndex.num_requested_indices],
                    "unique misses / requested indices": uvm_cache_stats[
                        UVMCacheStatsIndex.num_unique_misses
                    ]
                    / uvm_cache_stats[UVMCacheStatsIndex.num_requested_indices],
                }
            )
        self.log(f"uvm_cache_stats={m}")

    @torch.jit.ignore
    def _report_uvm_cache_stats(self) -> None:
        if self.stats_reporter is None:
            return
        stats_reporter: TBEStatsReporter = self.stats_reporter
        passed_steps = self.step - self.last_reported_step
        if passed_steps == 0:
            return
        if not stats_reporter.should_report(self.step):
            return

        uvm_cache_stats: List[float] = self.get_uvm_cache_stats(
            use_local_cache=False
        ).tolist()
        self.last_reported_step = self.step

        if len(self.last_reported_uvm_stats) == 0:
            self.last_reported_uvm_stats = [0.0] * len(uvm_cache_stats)
        uvm_cache_stats_delta: List[float] = [0.0] * len(uvm_cache_stats)
        for i in range(len(uvm_cache_stats)):
            uvm_cache_stats_delta[i] = (
                uvm_cache_stats[i] - self.last_reported_uvm_stats[i]
            )
        self.last_reported_uvm_stats = uvm_cache_stats

        element_size = self.lxu_cache_weights.element_size()
        for stat_index in UVMCacheStatsIndex:
            stats_reporter.report_data_amount(
                iteration_step=self.step,
                event_name=f"tbe.prefetch.cache_stats_by_data_size.{stat_index.name.lower()}",
                data_bytes=int(
                    uvm_cache_stats_delta[stat_index.value]
                    * element_size
                    * self.max_D_cache
                    / passed_steps
                ),
                embedding_id=self.logging_table_name,
                tbe_id=self.uuid,
            )

    def prefetch(
        self,
        indices: Tensor,
        offsets: Tensor,
        forward_stream: Optional[torch.cuda.Stream] = None,
        batch_size_per_feature_per_rank: Optional[List[List[int]]] = None,
    ) -> None:
        if self.prefetch_stream is None and forward_stream is not None:
            self.prefetch_stream = torch.cuda.current_stream()
            assert (
                self.prefetch_stream != forward_stream
            ), "prefetch_stream and forward_stream should not be the same stream"
        vbe_metadata = self._generate_vbe_metadata(
            offsets, batch_size_per_feature_per_rank
        )
        self._prefetch(
            indices,
            offsets,
            vbe_metadata,
            multipass_prefetch_config=self.multipass_prefetch_config,
        )
        if forward_stream is not None:
            self._prefetch_tensors_record_stream(forward_stream)

    def _prefetch(
        self,
        indices: Tensor,
        offsets: Tensor,
        vbe_metadata: Optional[invokers.lookup_args.VBEMetadata] = None,
        multipass_prefetch_config: Optional[MultiPassPrefetchConfig] = None,
    ) -> None:
        if not is_torchdynamo_compiling():
            # Mutations of nn.Module attr forces dynamo restart of Analysis which increases compilation time
            self.timestep += 1
            self.timesteps_prefetched.append(self.timestep)

        if not self.lxu_cache_weights.numel():
            return

        # Clear the local_uvm_cache_stats before the prefetch instead of after
        # the prefetch step, since it will be used in the CommonArgs in the
        # forward step
        if self.gather_uvm_cache_stats:
            self.local_uvm_cache_stats.zero_()
        self._report_io_size_count("prefetch_input", indices)

        final_lxu_cache_locations = torch.empty_like(indices, dtype=torch.int32)
        for (
            partial_indices,
            partial_lxu_cache_locations,
            base_offset,
        ) in self.get_prefetch_passes(
            multipass_prefetch_config, indices, final_lxu_cache_locations
        ):
            linear_cache_indices = torch.ops.fbgemm.linearize_cache_indices(
                self.cache_hash_size_cumsum,
                partial_indices,
                offsets,
                vbe_metadata.B_offsets if vbe_metadata is not None else None,
                vbe_metadata.max_B if vbe_metadata is not None else -1,
                base_offset,
            )

            if (
                self.record_cache_metrics.record_cache_miss_counter
                or self.record_cache_metrics.record_tablewise_cache_miss
            ):
                lxu_cache_locations = torch.ops.fbgemm.lxu_cache_lookup(
                    linear_cache_indices,
                    self.lxu_cache_state,
                    self.total_cache_hash_size,
                    self.gather_uvm_cache_stats,
                    self.local_uvm_cache_stats,
                )
                if self.record_cache_metrics.record_cache_miss_counter:
                    self._update_cache_miss_counter(
                        lxu_cache_locations, linear_cache_indices
                    )
                if self.record_cache_metrics.record_tablewise_cache_miss:
                    self._update_tablewise_cache_miss(
                        lxu_cache_locations, linear_cache_indices, offsets
                    )

            if self.cache_algorithm == CacheAlgorithm.LRU:
                torch.ops.fbgemm.lru_cache_populate(
                    self.weights_uvm,
                    self.cache_hash_size_cumsum,
                    self.total_cache_hash_size,
                    self.cache_index_table_map,
                    self.weights_offsets,
                    self.D_offsets,
                    linear_cache_indices,
                    self.lxu_cache_state,
                    self.lxu_cache_weights,
                    self.timestep,
                    self.lxu_state,
                    self.stochastic_rounding,
                    self.gather_uvm_cache_stats,
                    self.local_uvm_cache_stats,
                    self.lock_cache_line,
                    self.lxu_cache_locking_counter,
                )
            elif self.cache_algorithm == CacheAlgorithm.LFU:
                torch.ops.fbgemm.lfu_cache_populate(
                    self.weights_uvm,
                    self.cache_hash_size_cumsum,
                    self.total_cache_hash_size,
                    self.cache_index_table_map,
                    self.weights_offsets,
                    self.D_offsets,
                    linear_cache_indices,
                    self.lxu_cache_state,
                    self.lxu_cache_weights,
                    self.lxu_state,
                    self.stochastic_rounding,
                )

            torch.ops.fbgemm.lxu_cache_lookup(
                linear_cache_indices,
                self.lxu_cache_state,
                self.total_cache_hash_size,
                self.gather_uvm_cache_stats,
                self.local_uvm_cache_stats,
                lxu_cache_locations_output=partial_lxu_cache_locations,
            )

        assert (
            len(self.lxu_cache_locations_list) < self.max_prefetch_depth
        ), f"self.lxu_cache_locations_list has grown to size: {len(self.lxu_cache_locations_list)}, this exceeds the maximum: {self.max_prefetch_depth}. This probably indicates an error in logic where prefetch() is being called more frequently than forward()"
        self.lxu_cache_locations_list.append(final_lxu_cache_locations)

        if self.gather_uvm_cache_stats:
            # Accumulate local_uvm_cache_stats (int32) into uvm_cache_stats (int64).
            # We may want to do this accumulation atomically, but as it's only
            # for monitoring, slightly inaccurate result may be acceptable.
            self.uvm_cache_stats = torch.add(
                self.uvm_cache_stats, self.local_uvm_cache_stats
            )
            self._report_uvm_cache_stats()
            if self.should_log():
                self.print_uvm_cache_stats(use_local_cache=False)

    def should_log(self) -> bool:
        """Determines if we should log for this step, using exponentially decreasing frequency.

        Logs for steps: 100 200 ... 1,000 2,000 ... 10,000 20,000 ... 100,000 200,000 ...
        """
        s = self.step + 1  # step starts at 0
        return s >= 100 and s % (10 ** int(math.log10(s))) == 0

    def _prefetch_tensors_record_stream(
        self, forward_stream: torch.cuda.Stream
    ) -> None:
        # Record the tensors created by prefetch stream and consumed by forward/backward
        # to the forward stream. In PyTorch, each backward CUDA op runs on the same
        # stream that was used for its corresponding forward op.

        for t in self.lxu_cache_locations_list:
            t.record_stream(forward_stream)

    def _update_cache_miss_counter(
        self,
        lxu_cache_locations: Tensor,
        linear_cache_indices: Tensor,
    ) -> None:
        CACHE_MISS = -1
        CACHE_HIT = -2

        cache_missed_locations = torch.where(
            lxu_cache_locations == CACHE_MISS, linear_cache_indices, CACHE_HIT
        )
        unique_ids_list = torch.unique(cache_missed_locations)
        unique_ids_count_list = torch.where(unique_ids_list == CACHE_HIT, 0, 1)

        miss_count = torch.sum(unique_ids_count_list)

        self.cache_miss_counter[0] += (miss_count > 0).to(torch.int64)

        self.cache_miss_counter[1] += miss_count

    def _update_tablewise_cache_miss(
        self,
        lxu_cache_locations: Tensor,
        linear_cache_indices: Tensor,
        offsets: Tensor,
    ) -> None:
        CACHE_MISS = -1
        CACHE_HIT = -2

        num_tables = len(self.cache_hash_size_cumsum) - 1
        num_offsets_per_table = (len(offsets) - 1) // num_tables
        cache_missed_locations = torch.where(
            lxu_cache_locations == CACHE_MISS, linear_cache_indices, CACHE_HIT
        )

        for i in range(num_tables):
            start = offsets[i * num_offsets_per_table]
            end = offsets[(i + 1) * num_offsets_per_table]

            current_cache_missed_locations = cache_missed_locations[start:end]
            unique_ids_list = torch.unique(current_cache_missed_locations)
            unique_ids_count_list = torch.where(unique_ids_list == CACHE_HIT, 0, 1)

            miss_count = torch.sum(unique_ids_count_list)

            self.table_wise_cache_miss[i] += miss_count

    def init_embedding_weights_uniform(self, min_val: float, max_val: float) -> None:
        splits = self.split_embedding_weights()
        if self.weights_precision == SparseType.INT8:
            # TODO: add in-place FloatToFused8BitRowwiseQuantized conversion
            for emb in splits:
                assert (
                    len(emb.shape) == 2
                ), "Int8 embedding only supported for 2D weight tensors."
                shape = [emb.shape[0], emb.shape[1] - self.int8_emb_row_dim_offset]
                tmp_emb = torch.zeros(shape, device=self.current_device)
                tmp_emb.uniform_(min_val, max_val)
                tmp_emb_i8 = torch.ops.fbgemm.FloatToFused8BitRowwiseQuantized(tmp_emb)
                emb.data.copy_(tmp_emb_i8)
        else:
            for param in splits:
                param.uniform_(min_val, max_val)

    @torch.jit.ignore
    def split_embedding_weights(self) -> List[Tensor]:
        """
        Returns a list of weights, split by table
        """
        splits = []
        for t, (rows, dim, _, _) in enumerate(self.embedding_specs):
            if self.weights_precision == SparseType.INT8:
                dim += self.int8_emb_row_dim_offset
            placement = self.weights_physical_placements[t]
            offset = self.weights_physical_offsets[t]
            if placement == EmbeddingLocation.DEVICE.value:
                weights = self.weights_dev
            elif placement == EmbeddingLocation.HOST.value:
                weights = self.weights_host
            else:
                weights = self.weights_uvm
            if weights.dim() == 2:
                weights = weights.flatten()
            splits.append(
                weights.detach()[offset : offset + rows * dim].view(rows, dim)
            )
        return splits

    @torch.jit.ignore
    def get_optimizer_buffer(self, state: str) -> torch.Tensor:
        if self.optimizer == OptimType.NONE:
            raise NotImplementedError(
                f"Getting optimizer buffer is not supported for {self.optimizer}"
            )
        for name, buffer in self.named_buffers():
            if name == state:
                return buffer
        return torch.tensor(0)

    @torch.jit.export
    def get_optimizer_state(self) -> List[Dict[str, torch.Tensor]]:
        r"""
        Get the optimizer state dict that matches the OSS Pytorch optims
        TODO: populate the supported list of optimizers
        """
        split_optimizer_states = self.split_optimizer_states()
        if (
            self.optimizer == OptimType.EXACT_ROWWISE_ADAGRAD
            or self.optimizer == OptimType.EXACT_ADAGRAD
        ):
            list_of_state_dict = [
                (
                    {"sum": states[0], "prev_iter": states[1], "row_counter": states[2]}
                    if self._used_rowwise_adagrad_with_counter
                    else (
                        {"sum": states[0], "prev_iter": states[1]}
                        if self._used_rowwise_adagrad_with_global_weight_decay
                        else {"sum": states[0]}
                    )
                )
                for states in split_optimizer_states
            ]
        elif self.optimizer == OptimType.SGD or self.optimizer == OptimType.EXACT_SGD:
            list_of_state_dict = [
                {"momentum_buffer": states[0]} for states in split_optimizer_states
            ]
        elif (
            self.optimizer == OptimType.ADAM
            or self.optimizer == OptimType.PARTIAL_ROWWISE_ADAM
            or self.optimizer == OptimType.LAMB
            or self.optimizer == OptimType.PARTIAL_ROWWISE_LAMB
        ):
            list_of_state_dict = [
                {"exp_avg": states[0], "exp_avg_sq": states[1]}
                for states in split_optimizer_states
            ]
        else:
            raise NotImplementedError(
                f"Getting optimizer state {self.optimizer} is not implmeneted"
            )

        return list_of_state_dict

    @torch.jit.ignore
    def split_optimizer_states(
        self,
    ) -> List[List[torch.Tensor]]:
        """
        Returns a list of states, split by table
        """
        if self.optimizer == OptimType.NONE:
            raise NotImplementedError(
                f"Getting optimizer states is not supported for {self.optimizer}"
            )

        def get_optimizer_states(
            state_dev: Tensor,
            state_host: Tensor,
            state_uvm: Tensor,
            state_offsets: Tensor,
            state_placements: Tensor,
            rowwise: bool,
        ) -> List[torch.Tensor]:
            splits = []
            for t, (rows, dim, _, _) in enumerate(self.embedding_specs):
                offset = state_offsets[t]
                placement = state_placements[t]
                if placement == EmbeddingLocation.DEVICE:
                    state = state_dev
                elif placement == EmbeddingLocation.HOST:
                    state = state_host
                else:
                    state = state_uvm
                if not rowwise:
                    splits.append(
                        state.detach()[offset : offset + rows * dim].view(rows, dim)
                    )
                else:
                    splits.append(state.detach()[offset : offset + rows].view(rows))
            return splits

        states: List[List[torch.Tensor]] = []
        if self.optimizer not in (OptimType.EXACT_SGD,):
            states.append(
                get_optimizer_states(
                    self.momentum1_dev,
                    self.momentum1_host,
                    self.momentum1_uvm,
                    self.momentum1_physical_offsets,
                    self.momentum1_physical_placements,
                    rowwise=self.optimizer
                    in [
                        OptimType.EXACT_ROWWISE_ADAGRAD,
                    ],
                )
            )
        if self.optimizer in (
            OptimType.ADAM,
            OptimType.PARTIAL_ROWWISE_ADAM,
            OptimType.LAMB,
            OptimType.PARTIAL_ROWWISE_LAMB,
        ):
            states.append(
                get_optimizer_states(
                    self.momentum2_dev,
                    self.momentum2_host,
                    self.momentum2_uvm,
                    self.momentum2_physical_offsets,
                    self.momentum2_physical_placements,
                    rowwise=self.optimizer
                    in (OptimType.PARTIAL_ROWWISE_ADAM, OptimType.PARTIAL_ROWWISE_LAMB),
                )
            )
        if self._used_rowwise_adagrad_with_global_weight_decay:
            states.append(
                get_optimizer_states(
                    self.prev_iter_dev,
                    self.prev_iter_host,
                    self.prev_iter_uvm,
                    self.prev_iter_physical_offsets,
                    self.prev_iter_physical_placements,
                    rowwise=True,
                )
            )
        if self._used_rowwise_adagrad_with_counter:
            states.append(
                get_optimizer_states(
                    self.prev_iter_dev,
                    self.prev_iter_host,
                    self.prev_iter_uvm,
                    self.prev_iter_physical_offsets,
                    self.prev_iter_physical_placements,
                    rowwise=True,
                )
            )
            states.append(
                get_optimizer_states(
                    self.row_counter_dev,
                    self.row_counter_host,
                    self.row_counter_uvm,
                    self.row_counter_physical_offsets,
                    self.row_counter_physical_placements,
                    rowwise=True,
                )
            )
        return_states = [list(s) for s in zip(*states)]
        return return_states

    @torch.jit.export
    def set_learning_rate(self, lr: float) -> None:
        """
        Sets the learning rate.
        """
        if self.optimizer == OptimType.NONE:
            raise NotImplementedError(
                f"Setting learning rate is not supported for {self.optimizer}"
            )
        self._set_learning_rate(lr)

    @torch.jit.ignore
    def _set_learning_rate(self, lr: float) -> float:
        """
        Helper function to script `set_learning_rate`.
        Note that returning None does not work.
        """
        self.optimizer_args = self.optimizer_args._replace(learning_rate=lr)
        return 0.0

    @torch.jit.ignore
    def set_optimizer_step(self, step: int) -> None:
        """
        Sets the optimizer step.
        """
        self.log(f"set_optimizer_step from {self.iter[0]} to {step}")
        if self.optimizer == OptimType.NONE:
            raise NotImplementedError(
                f"Setting optimizer step is not supported for {self.optimizer}"
            )
        self.iter[0] = step

    @torch.jit.export
    def flush(self) -> None:
        if not self.lxu_cache_weights.numel():
            return
        torch.ops.fbgemm.lxu_cache_flush(
            self.weights_uvm,
            self.cache_hash_size_cumsum,
            self.cache_index_table_map,
            self.weights_offsets,
            self.D_offsets,
            self.total_D,
            self.lxu_cache_state,
            self.lxu_cache_weights,
            self.stochastic_rounding,
        )

    def _apply_split(
        self,
        split: SplitState,
        prefix: str,
        dtype: Type[torch.dtype],
        enforce_hbm: bool = False,
        make_dev_param: bool = False,
        dev_reshape: Optional[Tuple[int, ...]] = None,
    ) -> None:
        apply_split_helper(
            self.register_buffer,
            functools.partial(setattr, self),
            self.current_device,
            self.use_cpu,
            self.feature_table_map,
            split,
            prefix,
            dtype,
            enforce_hbm,
            make_dev_param,
            dev_reshape,
            self._uvm_tensors_log,
        )

    def _apply_cache_state(
        self,
        cache_state: CacheState,
        cache_algorithm: CacheAlgorithm,
        cache_load_factor: float,
        cache_sets: int,
        cache_reserved_memory: float,
        dtype: torch.dtype,
    ) -> None:
        self.cache_algorithm = cache_algorithm
        self.timestep = 1
        self.timesteps_prefetched = []

        self.max_prefetch_depth = MAX_PREFETCH_DEPTH
        self.lxu_cache_locations_list = []
        self.lxu_cache_locations_empty = torch.empty(
            0, device=self.current_device, dtype=torch.int32
        ).fill_(-1)
        self.lxu_cache_locations = self.lxu_cache_locations_empty
        self._indices = self.lxu_cache_locations_empty
        self._offsets = self.lxu_cache_locations_empty
        self._vbe_B_offsets = self.lxu_cache_locations_empty
        self._vbe_max_B = -1
        self.prefetch_stream: Optional[torch.cuda.Stream] = None

        self._init_uvm_cache_stats()

        # NOTE: no cache for CPU mode!
        if cache_state.total_cache_hash_size == 0 or self.use_cpu:
            self.register_buffer(
                "lxu_cache_weights",
                torch.zeros(0, 0, device=self.current_device, dtype=dtype),
            )
            # NOTE: make TorchScript work!
            self.register_buffer(
                "cache_hash_size_cumsum",
                torch.zeros(1, dtype=torch.int64, device=self.current_device),
                persistent=False,
            )
            self.register_buffer(
                "total_cache_hash_size",
                torch.zeros(1, dtype=torch.int64, device=self.current_device),
                persistent=False,
            )
            self.register_buffer(
                "cache_index_table_map",
                torch.zeros(1, dtype=torch.int64, device=self.current_device),
                persistent=False,
            )
            self.register_buffer(
                "lxu_cache_state",
                torch.zeros(1, dtype=torch.int64, device=self.current_device),
                persistent=False,
            )
            self.register_buffer(
                "lxu_state",
                torch.zeros(1, dtype=torch.int64, device=self.current_device),
                persistent=False,
            )
            self.register_buffer(
                "cache_miss_counter",
                torch.tensor([0, 0], dtype=torch.int64),
                persistent=False,
            )
            self._init_uvm_cache_counter(cache_sets, persistent=False)
            return

        assert cache_load_factor > 0
        element_size = 2 if dtype == torch.float16 else 4
        if cache_sets <= 0:
            total_memory = torch.cuda.get_device_properties(
                self.current_device
            ).total_memory
            free_memory = (
                total_memory
                - torch.cuda.memory_reserved(self.current_device)
                - int(cache_reserved_memory)
            )
            assert free_memory > 0
            cache_sets = (
                int(cache_state.total_cache_hash_size * cache_load_factor)
                + DEFAULT_ASSOC
                - 1
            ) // DEFAULT_ASSOC
            cache_sets = 1 if cache_sets == 0 else cache_sets
            cache_size = cache_sets * DEFAULT_ASSOC * element_size * self.max_D_cache
            if cache_size > free_memory:
                cache_sets = (
                    int(1.0 * free_memory / self.max_D_cache / element_size)
                    + DEFAULT_ASSOC
                    - 1
                ) // DEFAULT_ASSOC
        cache_load_factor = (
            1.0 * cache_sets * DEFAULT_ASSOC / int(cache_state.total_cache_hash_size)
        )
        assert cache_sets > 0
        if cache_algorithm == CacheAlgorithm.LFU:
            assert cache_sets < 2**24 - 1
        cache_size = cache_sets * DEFAULT_ASSOC * element_size * self.max_D_cache
        self.log(
            f"Using on-device cache with admission algorithm "
            f"{cache_algorithm}, {cache_sets} sets, "
            f"load_factor: {cache_load_factor : .3f}, "
            f"cache_size: {cache_size / 1024.0 / 1024.0 / 1024.0 : .2f}GB, "
            f"cache_precision: {dtype}"
        )

        self.total_cache_hash_size = cache_state.total_cache_hash_size
        self.register_buffer(
            "cache_hash_size_cumsum",
            torch.tensor(
                cache_state.cache_hash_size_cumsum,
                device=self.current_device,
                dtype=torch.int64,
            ),
        )
        self.register_buffer(
            "cache_index_table_map",
            torch.tensor(
                cache_state.cache_index_table_map,
                device=self.current_device,
                dtype=torch.int32,
            ),
        )
        self.register_buffer(
            "lxu_cache_state",
            torch.zeros(
                cache_sets, DEFAULT_ASSOC, device=self.current_device, dtype=torch.int64
            ).fill_(-1),
        )
        self.register_buffer(
            "lxu_cache_weights",
            torch.zeros(
                cache_sets * DEFAULT_ASSOC,
                self.max_D_cache,
                device=self.current_device,
                dtype=dtype,
            ),
        )
        self.register_buffer(
            "lxu_state",
            torch.zeros(
                size=(
                    (self.total_cache_hash_size + 1,)
                    if cache_algorithm == CacheAlgorithm.LFU
                    else (cache_sets, DEFAULT_ASSOC)
                ),
                device=self.current_device,
                dtype=torch.int64,
            ),
        )
        self.register_buffer(
            "cache_miss_counter",
            torch.tensor([0, 0], device=self.current_device, dtype=torch.int64),
        )
        self._init_uvm_cache_counter(cache_sets, persistent=True)
        if self.prefetch_pipeline:
            # using the placeholder_autograd_tensor to make sure
            # the hook is executed after the backward pass
            # not using register_module_full_backward_hook
            # due to https://github.com/pytorch/pytorch/issues/100528
            self.placeholder_autograd_tensor.register_hook(
                self._sync_stream_post_backward
            )
            self.register_full_backward_pre_hook(
                self._update_cache_counter_and_locations
            )

        if cache_algorithm not in (CacheAlgorithm.LFU, CacheAlgorithm.LRU):
            raise ValueError(
                f"cache_algorithm must be {CacheAlgorithm.LRU} "
                f"or {CacheAlgorithm.LFU}"
            )

    # pyre-ignore
    def _recording_to_timer(
        self, timer: Optional[AsyncSeriesTimer], **kwargs: Any
    ) -> Any:
        if self.stats_reporter is not None and self.stats_reporter.should_report(
            self.step
        ):
            assert (
                timer
            ), "We shouldn't be here, async timer must have been initiated if reporter is present."
            return timer.recording(**kwargs)
        # No-Op context manager
        return contextlib.nullcontext()

    def _sync_stream_post_backward(
        self,
        grad: Tensor,
    ) -> None:
        """
        backward hook function when prefetch_pipeline is enabled.

        With the pipeline, prefetch(batch_{i+2}) may overlap with backward(batch_{i}).
        There is race condition that backward(batch_i) writes to UVM memory and
        at the same time prefetch(batch_{i+2}) loads UVM memory to cache. This stream sync forces
        backward(batch_i) to finish before prefetch(batch_{i+2}).
        """
        if self.prefetch_stream is not None:
            self.prefetch_stream.wait_stream(torch.cuda.current_stream())

    def _update_cache_counter_and_locations(
        self,
        module: nn.Module,
        grad_input: Union[Tuple[Tensor, ...], Tensor],
    ) -> None:
        """
        Backward prehook function when prefetch_pipeline is enabled.

        This function does 3 things:
        1. backward stream waits for prefetch stream to finish.
        Otherwise the prefetch(batch_{i+1}) might overlap with backward(batch_i).
        If an idx is not in cache in batch_i, but it is being inserted in batch_{i+1},
        there is race condition that backward(batch_i) writes to UVM memory and
        at the same time prefetch(batch_{i+1}) loads UVM memory to cache.

        2. decrement the lxu_cache_locking_counter to indicate the current batch is finished.
        The lxu_cache_locking_counter is updated in both prefetch and TBE backward.
        As there is no overlap between prefetch and backward, we can decrement either before or
        after backward. It's better to decrement before lxu_cache_locations gets updated.

        3. update lxu_cache_locations to address the cache inconsistency issue.
        In the case that the same index is not inserted into cache in batch_i,
        but it is inserted in batch_{i+1}, the cache can be invalid in
        the sense that the cached weight for this index does not have the
        backward update of batch_i.

        Example of the issue is as follows:
        idx is in batch_i, batch_{i+1}
        prefetch(batch_i)
          - failed to insert idx into cache, cache_locations_batch_i of idx is -1 (cache miss)
        forward(batch_i)
        prefetch(batch_{i+1})
          - insert idx into cache, cache is loaded from host memory
        backward(batch_i)
          - cache_locations_batch_i of idx is -1, the host memory is updated
        forward(batch_{i+1})
          - OUTPUT IS WRONG. the weight for idx is fetched from cache, but the cache is outdated.

        The fix to this cache inconsistency is to update the cache_locations_batch_i before backward of batch_i,
        so that the cache gets updated correctly by the backward pass of TBE.
        """

        if self.prefetch_stream is not None:
            # need to wait for the prefetch of next batch,
            # so that cache states are valid
            with self._recording_to_timer(
                self.bwd_wait_prefetch_timer,
                context=self.step,
                stream=torch.cuda.current_stream(),
            ):
                torch.cuda.current_stream().wait_stream(self.prefetch_stream)

        torch.ops.fbgemm.lxu_cache_locking_counter_decrement(
            self.lxu_cache_locking_counter,
            self.lxu_cache_locations,
        )
        # Recompute linear_cache_indices
        linear_cache_indices = torch.ops.fbgemm.linearize_cache_indices(
            self.cache_hash_size_cumsum,
            self._indices,
            self._offsets,
            self._vbe_B_offsets,
            self._vbe_max_B,
        )
        (
            linear_unique_indices,
            linear_unique_indices_length,
            _,
        ) = torch.ops.fbgemm.get_unique_indices(
            linear_cache_indices,
            self.total_cache_hash_size,
            compute_count=False,
        )
        torch.ops.fbgemm.lxu_cache_lookup(
            linear_unique_indices,
            self.lxu_cache_state,
            self.total_cache_hash_size,
            gather_cache_stats=False,  # not collecting cache stats
            num_uniq_cache_indices=linear_unique_indices_length,
            lxu_cache_locations_output=self.lxu_cache_locations,
        )

    def _init_uvm_cache_counter(self, cache_sets: int, persistent: bool) -> None:
        if self.prefetch_pipeline and persistent:
            self.register_buffer(
                "lxu_cache_locking_counter",
                torch.zeros(
                    cache_sets,
                    DEFAULT_ASSOC,
                    device=self.current_device,
                    dtype=torch.int32,
                ),
            )
        else:
            self.register_buffer(
                "lxu_cache_locking_counter",
                torch.zeros([0, 0], dtype=torch.int32, device=self.current_device),
                persistent=persistent,
            )

    def _init_uvm_cache_stats(self) -> None:
        if not self.gather_uvm_cache_stats:
            # If uvm_cache_stats is not enabled, register stub entries via buffer to state_dict for TorchScript to JIT properly.
            # Since we're not using these variables, we can choose minimize tensor size to keep state_dict size small.
            self.register_buffer(
                "uvm_cache_stats",
                torch.zeros(
                    1,
                    device=self.current_device,
                    dtype=torch.int64,
                ),
                persistent=False,
            )
            self.register_buffer(
                "local_uvm_cache_stats",
                torch.zeros(
                    1,
                    device=self.current_device,
                    dtype=torch.int32,
                ),
                persistent=False,
            )
        else:
            self.register_buffer(
                "uvm_cache_stats",
                torch.zeros(
                    size=(self.uvm_cache_stats_size,),
                    device=self.current_device,
                    dtype=torch.int64,
                ),
            )
            self.register_buffer(
                "local_uvm_cache_stats",
                torch.zeros(
                    size=(self.uvm_cache_stats_size,),
                    device=self.current_device,
                    dtype=torch.int32,
                ),
            )
            self.reset_uvm_cache_stats()
        self.last_uvm_cache_print_state = torch.zeros_like(self.uvm_cache_stats)

    def reset_cache_states(self) -> None:
        if not self.lxu_cache_weights.numel():
            return
        self.lxu_cache_state.fill_(-1)
        self.lxu_state.fill_(0)
        self.timestep = 1

    def reset_embedding_weight_momentum(
        self,
        pruned_indices: Tensor,
        pruned_indices_offsets: Tensor,
        logical_table_ids: Tensor,
        buffer_ids: Tensor,
    ) -> None:
        if self.optimizer == OptimType.NONE:
            raise NotImplementedError(
                f"Resetting embedding weight momentum is not supported for {self.optimizer}"
            )
        total_cache_hash_size = 0
        if isinstance(self.total_cache_hash_size, Tensor):
            total_cache_hash_size = self.total_cache_hash_size.item()
        else:
            total_cache_hash_size = self.total_cache_hash_size

        rowwise = self.optimizer in [
            OptimType.EXACT_ROWWISE_ADAGRAD,
        ]
        if rowwise:
            torch.ops.fbgemm.reset_weight_momentum(
                dev_weights=self.weights_dev,
                uvm_weights=self.weights_uvm,
                lxu_cache_weights=self.lxu_cache_weights,
                weights_placements=self.weights_placements,
                weights_offsets=self.weights_offsets,
                momentum1_dev=self.momentum1_dev,
                momentum1_uvm=self.momentum1_uvm,
                momentum1_placements=self.momentum1_placements,
                momentum1_offsets=self.momentum1_offsets,
                D_offsets=self.D_offsets,
                pruned_indices=pruned_indices.to(device=self.current_device),
                pruned_indices_offsets=pruned_indices_offsets.to(
                    device=self.current_device
                ),
                logical_table_ids=logical_table_ids.to(device=self.current_device),
                buffer_ids=buffer_ids.to(device=self.current_device),
                cache_hash_size_cumsum=self.cache_hash_size_cumsum,
                lxu_cache_state=self.lxu_cache_state,
                total_cache_hash_size=total_cache_hash_size,
            )


class DenseTableBatchedEmbeddingBagsCodegen(nn.Module):
    """
    Table-batched version of nn.EmbeddingBag(sparse=False)
    """

    weights: Tensor
    weights_offsets: Tensor
    D_offsets: Tensor
    total_D: int
    max_D: int
    hash_size_cumsum: Tensor
    total_hash_size_bits: int
    embedding_specs: List[Tuple[int, int]]

    def __init__(
        self,
        embedding_specs: List[Tuple[int, int]],  # tuple of (rows, dims)
        feature_table_map: Optional[List[int]] = None,  # [T]
        weights_precision: SparseType = SparseType.FP32,
        pooling_mode: PoolingMode = PoolingMode.SUM,
        use_cpu: bool = False,
        output_dtype: SparseType = SparseType.FP32,
        use_mtia: bool = False,
    ) -> None:  # noqa C901  # tuple of (rows, dims,)
        super(DenseTableBatchedEmbeddingBagsCodegen, self).__init__()

        self.pooling_mode = pooling_mode
        self.weights_precision = weights_precision
        self.output_dtype: int = output_dtype.as_int()
        table_embedding_dtype = weights_precision.as_dtype()

        self.use_cpu: bool = use_cpu
        self.use_mtia: bool = use_mtia

        assert not (use_cpu and use_mtia), "Cannot use CPU and MTIA at the same time"

        if self.use_cpu or self.pooling_mode == PoolingMode.NONE:
            assert output_dtype in [
                SparseType.FP32,
                SparseType.FP16,
                SparseType.BF16,
            ], "Fused pooled embedding quantization only supported for cuda."

        # pyre-fixme[8]: Attribute has type `device`; used as `Union[int, device]`.
        self.current_device: torch.device = (
            torch.device("cpu")
            if self.use_cpu
            else (
                torch.device(f"mtia:{torch.mtia.current_device()}")
                if self.use_mtia
                else torch.cuda.current_device()
            )
        )

        self.embedding_specs = embedding_specs
        (rows, dims) = zip(*embedding_specs)
        T_ = len(self.embedding_specs)
        assert T_ > 0

        feature_table_map = (
            feature_table_map if feature_table_map is not None else list(range(T_))
        )
        T = len(feature_table_map)
        assert T_ <= T

        feature_dims = [dims[t] for t in feature_table_map]
        D_offsets = [0] + list(accumulate(feature_dims))
        self.total_D = D_offsets[-1]
        self.max_D = max(dims)
        self.register_buffer(
            "D_offsets",
            torch.tensor(D_offsets, device=self.current_device, dtype=torch.int32),
        )
        assert self.D_offsets.numel() == T + 1
        # Required for VBE
        self.register_buffer(
            "feature_dims",
            torch.tensor(feature_dims, device="cpu", dtype=torch.int64),
        )

        hash_size_cumsum = [0] + list(accumulate(rows))
        if hash_size_cumsum[-1] == 0:
            self.total_hash_size_bits: int = 0
        else:
            self.total_hash_size_bits: int = int(log2(float(hash_size_cumsum[-1])) + 1)
        # The last element is to easily access # of rows of each table by
        # hash_size_cumsum[t + 1] - hash_size_cumsum[t]
        hash_size_cumsum = [hash_size_cumsum[t] for t in feature_table_map] + [
            hash_size_cumsum[-1]
        ]
        self.register_buffer(
            "hash_size_cumsum",
            torch.tensor(
                hash_size_cumsum, device=self.current_device, dtype=torch.int64
            ),
        )
        weights_offsets = [0] + list(
            accumulate([row * dim for (row, dim) in embedding_specs])
        )
        self.weights = nn.Parameter(
            torch.randn(
                weights_offsets[-1],
                device=self.current_device,
                dtype=table_embedding_dtype,
            )
        )
        for feature in range(T):
            t = feature_table_map[feature]
            row, dim = embedding_specs[t]
            if (
                self.weights[weights_offsets[t] : weights_offsets[t + 1]].numel()
                != row * dim
            ):
                logging.info(
                    f"row {row} dim {dim} feature {feature} t {t} {self.weights[weights_offsets[t] : weights_offsets[t + 1]].numel()}"
                )
            assert (
                self.weights[weights_offsets[t] : weights_offsets[t + 1]].numel()
                == row * dim
            )
            assert self.hash_size_cumsum[feature] == sum(
                row for (row, _) in embedding_specs[:t]
            )

        self.weights_physical_offsets: List[int] = weights_offsets
        weights_offsets = [weights_offsets[t] for t in feature_table_map]
        self.register_buffer(
            "weights_offsets",
            torch.tensor(
                weights_offsets, device=self.current_device, dtype=torch.int64
            ),
        )

    @torch.jit.ignore
    def _generate_vbe_metadata(
        self,
        offsets: Tensor,
        batch_size_per_feature_per_rank: Optional[List[List[int]]],
    ) -> invokers.lookup_args.VBEMetadata:
        # Blocking D2H copy, but only runs at first call
        self.feature_dims = self.feature_dims.cpu()
        return generate_vbe_metadata(
            offsets,
            batch_size_per_feature_per_rank,
            OptimType.NONE,
            self.pooling_mode,
            self.feature_dims,
            self.current_device,
        )

    def forward(
        self,
        indices: Tensor,
        offsets: Tensor,
        per_sample_weights: Optional[Tensor] = None,
        feature_requires_grad: Optional[Tensor] = None,
        batch_size_per_feature_per_rank: Optional[List[List[int]]] = None,
    ) -> Tensor:
        # Generate VBE metadata
        vbe_metadata = self._generate_vbe_metadata(
            offsets, batch_size_per_feature_per_rank
        )

        (indices, offsets) = indices.long(), offsets.long()
        # Force casting per_sample_weights to float
        if per_sample_weights is not None:
            per_sample_weights = per_sample_weights.float()

        return torch.ops.fbgemm.dense_embedding_codegen_lookup_function(
            dev_weights=self.weights,
            weights_offsets=self.weights_offsets,
            D_offsets=self.D_offsets,
            total_D=self.total_D,
            max_D=self.max_D,
            hash_size_cumsum=self.hash_size_cumsum,
            total_hash_size_bits=self.total_hash_size_bits,
            indices=indices,
            offsets=offsets,
            pooling_mode=self.pooling_mode,
            indice_weights=per_sample_weights,
            feature_requires_grad=feature_requires_grad,
            output_dtype=self.output_dtype,
            B_offsets=vbe_metadata.B_offsets,
            vbe_output_offsets_feature_rank=vbe_metadata.output_offsets_feature_rank,
            vbe_B_offsets_rank_per_feature=vbe_metadata.B_offsets_rank_per_feature,
            max_B=vbe_metadata.max_B,
            max_B_feature_rank=vbe_metadata.max_B_feature_rank,
            vbe_output_size=vbe_metadata.output_size,
        )

    @torch.jit.export
    def split_embedding_weights(self) -> List[Tensor]:
        """
        Returns a list of weights, split by table
        """
        splits = []
        for t, (rows, dim) in enumerate(self.embedding_specs):
            offset = self.weights_physical_offsets[t]
            splits.append(
                self.weights.detach()[offset : offset + rows * dim].view(rows, dim)
            )
        return splits

    def init_embedding_weights_uniform(self, min_val: float, max_val: float) -> None:
        splits = self.split_embedding_weights()
        for param in splits:
            param.uniform_(min_val, max_val)
