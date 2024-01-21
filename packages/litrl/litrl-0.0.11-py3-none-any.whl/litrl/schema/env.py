from typing import Generic

from pydantic.dataclasses import dataclass as pydantic_dataclass

from litrl.env.type_vars import EnvType
from litrl.schema.agent import AgentSchema, MCTSAgentSchema
from litrl.schema.instantiator import InstantiatorClass


@pydantic_dataclass(frozen=True)
class EnvSchema(InstantiatorClass[EnvType], Generic[EnvType]):
    id: str  # noqa: A003
    opponent: None | AgentSchema | MCTSAgentSchema = None
    val: bool | None = None
