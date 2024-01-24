from copy import deepcopy
from typing import Any, TypeAlias

try:
    from typing import Self
except ImportError:
    from typing_extensions import Self

from litrl.algo.mcts.edge import Edge
from litrl.algo.mcts.node import Node
from litrl.env.typing import MultiAgentEnv

MctsActionType: TypeAlias = int
AnyNode: TypeAlias = Node[Edge] | Node[None]


class MultiAgentMctsEnv(MultiAgentEnv[Any, Any, Any]):
    def copy(self) -> Self:
        return deepcopy(self)
