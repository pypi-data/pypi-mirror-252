from fairseq.dataclass.configs import (
    FairseqDataclass,
    CommonConfig,
    CommonEvalConfig,
    DistributedTrainingConfig,
    DatasetConfig,
    OptimizationConfig,
    CheckpointConfig,
    FairseqBMUFConfig,
    GenerationConfig,
    EvalLMConfig,
    InteractiveConfig,
    EMAConfig,
)

from dataclasses import dataclass, field
from typing import Any
from omegaconf import MISSING


@dataclass
class PatchedFairseqConfig(FairseqDataclass):
    common: CommonConfig = field(default=CommonConfig)
    common_eval: CommonEvalConfig = field(default=CommonEvalConfig)
    distributed_training: DistributedTrainingConfig = field(
        default=DistributedTrainingConfig
    )
    dataset: DatasetConfig = field(default=DatasetConfig)
    optimization: OptimizationConfig = field(default=OptimizationConfig)
    checkpoint: CheckpointConfig = field(default=CheckpointConfig)
    bmuf: FairseqBMUFConfig = field(default=FairseqBMUFConfig)
    generation: GenerationConfig = field(default=GenerationConfig)
    eval_lm: EvalLMConfig = field(default=EvalLMConfig)
    interactive: InteractiveConfig = field(default=InteractiveConfig)
    model: Any = MISSING
    task: Any = None
    criterion: Any = None
    optimizer: Any = None
    lr_scheduler: Any = None
    scoring: Any = None
    bpe: Any = None
    tokenizer: Any = None
    ema: EMAConfig = field(default=EMAConfig)


print("patched fairseq")
FairseqConfig = PatchedFairseqConfig
