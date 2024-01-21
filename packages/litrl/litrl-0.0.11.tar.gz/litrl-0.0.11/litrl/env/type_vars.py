from typing import Any, Literal, TypeVar

from litrl.env.typing import MultiAgentEnv, SingleAgentEnv

SingleAgentId = Literal["cartpole", "lunar_lander", "breakout"]
MultiAgentId = Literal["connect_four"]
EnvId = SingleAgentId | MultiAgentId

EnvType = TypeVar(
    "EnvType",
    bound=SingleAgentEnv[Any, Any] | MultiAgentEnv[Any, Any, Any],
)
