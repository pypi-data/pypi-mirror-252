from abc import ABC, abstractmethod
from typing import TYPE_CHECKING, Generic, Optional, TypeVar

from litrl.algo.mcts.edge import Edge
from litrl.algo.mcts.value import ValueStrategy, Winrate

if TYPE_CHECKING:
    from litrl.algo.mcts.typing import AnyNode, MctsActionType

EdgeType = TypeVar("EdgeType", Edge, None)


class Node(Generic[EdgeType], ABC):
    def __init__(
        self,
        parent_edge: EdgeType,
        value_strategy: ValueStrategy | None = None,
        exploration_coef: float = 1,
        *,
        root_player_turn: bool,
    ) -> None:
        if value_strategy is None:
            value_strategy = Winrate()
        self.parent_edge: EdgeType = parent_edge
        self.edges: dict["MctsActionType", Edge] = {}
        self.exploration_coef = exploration_coef
        self.value_strategy = value_strategy
        self.root_player_turn = root_player_turn

    def add_child(self, action: "MctsActionType") -> None:
        edge = Edge(parent=self)
        self.edges[action] = edge
        edge.child = ChildNode(parent_edge=edge)

    @property
    def visits(self) -> float:
        return sum(edge.visits for edge in self.edges.values())

    @property
    def reward_sum(self) -> float:
        return sum(edge.reward_sum for edge in self.edges.values())

    @property
    @abstractmethod
    def parent(self) -> Optional["AnyNode"]:
        raise NotImplementedError

    @property
    def n_children(self) -> int:
        return len(self.edges)

    @property
    def children(self) -> dict["MctsActionType", "ChildNode"]:
        return {action: edge.child for action, edge in self.edges.items()}


class Root(Node[None]):
    def __init__(self) -> None:
        super().__init__(parent_edge=None, root_player_turn=True)

    @property
    def parent(self) -> None:
        return None


class ChildNode(Node["Edge"]):
    def __init__(self, parent_edge: "Edge") -> None:
        super().__init__(
            parent_edge=parent_edge,
            root_player_turn=not parent_edge.parent.root_player_turn,
        )

    @property
    def parent(self) -> "AnyNode":
        return self.parent_edge.parent
