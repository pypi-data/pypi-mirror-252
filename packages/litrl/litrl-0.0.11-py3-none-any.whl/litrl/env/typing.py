import warnings
from abc import ABC
from typing import Generic, Literal, Protocol, Self, TypeAlias, TypedDict, TypeVar, runtime_checkable

with warnings.catch_warnings():
    warnings.filterwarnings(action="ignore", category=DeprecationWarning)
    from nptyping import Shape

from typing import Any, cast, get_args

from gymnasium.spaces import Space
from pettingzoo.utils import agent_selector

SingleAgentId = Literal["cartpole", "lunar_lander", "breakout"]
GYM_IDS = ["CartPole-v1", "BreakoutNoFrameskip-v4", "LunarLander-v2"]
MultiAgentId = Literal["connect_four"]
MULTI_AGENT_IDS = cast(list[MultiAgentId], get_args(MultiAgentId))
EnvId = SingleAgentId | MultiAgentId
GymId: TypeAlias = str
ActType = TypeVar("ActType")
ObsType = TypeVar("ObsType")
MaskType = TypeVar("MaskType")
ObsType_co = TypeVar("ObsType_co", covariant=True)

ObsShape = TypeVar("ObsShape", bound=Shape)
MaskShape = TypeVar("MaskShape")
AgentID = TypeVar("AgentID")


class MaskedObs(TypedDict, Generic[ObsType, MaskType]):
    obs: ObsType  # NDArray[ObsShape, Float64]
    action_mask: MaskType  # NDArray[Shape[MaskShape], Int64]


class MaskedInfo(TypedDict, Generic[MaskType]):
    action_mask: MaskType  # NDArray[MaskShape, Int64]


@runtime_checkable
class SingleAgentEnv(Protocol, Generic[ObsType_co, ActType]):
    """Gym environments interface.

    We use this class to facilitate typing consistency within the LitRL codebase.
    The API remains the same as in OpenAI Gym.
    """

    def get_wrapper_attr(self, attribute: str) -> Any:
        del attribute
        raise NotImplementedError

    @property
    def observation_space(self) -> Space[ObsType_co]:
        ...

    @property
    def action_space(self) -> Space[ActType]:
        ...

    def __init__(self, env_id: EnvId, **kwargs: Any) -> None:
        del env_id, kwargs
        ...

    def step(
        self,
        action: ActType,
    ) -> tuple[ObsType_co, float, bool, bool, dict[str, Any]]:
        ...

    def reset(
        self,
        seed: int | None = None,
        options: dict[str, Any] | None = None,
    ) -> tuple[ObsType_co, dict[str, Any]]:
        ...

    def close(self) -> None:
        ...


class OpponentEnv(
    SingleAgentEnv[ObsType_co, ActType],
    Protocol,
    Generic[ObsType_co, ActType],
):
    """Describes an SingleAgentEnv environment that was wrapped by the StaticOpponent wrapper."""


class MultiAgentEnv(ABC, Generic[ObsType_co, ActType, AgentID]):
    """PettingZoo environments are not very mature yet and yield unexpected bugs.

    LitRL environments follow the gym/pettingzoo API as closely as possible,
    but we ensure the environments are stable by converting them to a MultiAgentEnv class.
    """

    agent_selection: AgentID
    unwrapped: Self
    truncations: dict[str, int]
    terminations: dict[str, int]
    infos: dict[str, Any]
    _cumulative_rewards: dict[str, float]
    _agent_selector: agent_selector

    def step(self, action: ActType) -> None:
        del action
        raise NotImplementedError

    def last(self) -> tuple[ObsType_co, float, bool, bool, dict[str, Any]]:
        raise NotImplementedError

    def observe(self, agent: AgentID) -> ObsType_co:
        del agent
        raise NotImplementedError

    def action_space(self, agent: AgentID) -> Space[ActType]:
        del agent
        raise NotImplementedError

    def reset(
        self,
        seed: int | None = None,
        options: dict[str, Any] | None = None,
    ) -> None:
        del seed, options
        raise NotImplementedError

    def close(self) -> None:
        raise NotImplementedError
