import numpy as np

from litrl.algo.mcts.backpropagate import VanillaBackpropagate
from litrl.algo.mcts.node import Root
from litrl.algo.mcts.select import VanillaSelection
from litrl.algo.mcts.typing import MultiAgentMctsEnv

from .mcts_config import MCTSConfig, MCTSConfigBuilder


class MCTS:
    def __init__(
        self,
        env: MultiAgentMctsEnv,
        cfg: MCTSConfig | None = None,
    ) -> None:
        cfg = cfg if cfg is not None else MCTSConfigBuilder().build()
        self._cfg = cfg
        self._np_random = np.random.default_rng(seed=cfg.seed)
        self.root = Root(env)
        self._cfg.expansion_strategy.expand(self.root.env, self.root)

    def simulate(self) -> None:
        temp_env = self.root.env.copy()
        node = self._cfg.selection_strategy.select_and_step(
            temp_env,
            self.root,
        )
        self._cfg.expansion_strategy.expand(temp_env, node)
        reward = self._cfg.rollout_strategy.rollout(
            temp_env,
            self.root.env.unwrapped.agent_selection,
        )
        self._cfg.backpropagate_strategy.backpropagate(node, reward)

    def get_action(self) -> int:
        for _ in range(self._cfg.simulations):
            self.simulate()

        return self._cfg.recommend_strategy.get_action(self.root)

    def update_root(self, action: int) -> None:
        self.root.new_root(action, self.root.env)
        if isinstance(self._cfg.selection_strategy, VanillaSelection):
            self._cfg.selection_strategy.root_depth = self.root.depth
        if isinstance(self._cfg.backpropagate_strategy, VanillaBackpropagate):
            self._cfg.backpropagate_strategy.root_depth = self.root.depth
