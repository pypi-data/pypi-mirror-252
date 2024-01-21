from typing import Any, TypeVar

from litrl.env.typing import MultiAgentEnv, SingleAgentEnv

EnvType = TypeVar(
    "EnvType",
    bound=SingleAgentEnv[Any, Any] | MultiAgentEnv[Any, Any, Any],
)
