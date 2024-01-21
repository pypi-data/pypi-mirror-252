from typing import Generic, Self

from pydantic import field_validator
from pydantic.dataclasses import dataclass as pydantic_dataclass

from litrl.env.type_vars import EnvType
from litrl.schema.env import EnvSchema


@pydantic_dataclass(frozen=True)
class BufferSchema:
    batch_size: int
    max_size: int


@pydantic_dataclass(frozen=True)
class ModelConfigSchema(Generic[EnvType]):
    seed: int
    lr: float
    gamma: float
    warm_start_steps: int
    hidden_size: int
    n_hidden_layers: int
    buffer: BufferSchema
    epsilon: float
    target_entropy: float
    tau: float
    env_fabric: EnvSchema[EnvType]
    val_env_fabric: EnvSchema[EnvType]

    @field_validator("lr")
    @classmethod
    def validate_lr(cls: type[Self], lr: float) -> float:
        if lr < 0:
            msg = f"'lr' can't be less than 0, got: {lr}"
            raise ValueError(msg)
        return lr
