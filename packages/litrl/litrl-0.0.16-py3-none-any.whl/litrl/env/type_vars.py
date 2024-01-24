from typing import Any, TypeVar

from litrl.env.typing import MultiAgentEnv, SingleAgentEnv

EnvType = TypeVar(  # TODO move somewhere else.
    "EnvType",
    bound=SingleAgentEnv[Any, Any] | MultiAgentEnv[Any, Any, Any],
)
