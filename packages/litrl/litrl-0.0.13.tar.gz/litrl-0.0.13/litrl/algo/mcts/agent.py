from litrl.algo.mcts.mcts import MCTS
from litrl.algo.mcts.mcts_config import MCTSConfig, MCTSConfigBuilder
from litrl.algo.mcts.typing import MultiAgentMctsEnv
from litrl.common.agent import Agent


class MCTSAgent(Agent[MultiAgentMctsEnv, int]):
    def __init__(
        self,
        cfg: MCTSConfig | None = None,
        *,
        prompt_action: bool = False,
    ) -> None:
        if cfg is None:
            cfg = MCTSConfigBuilder().build()
        super().__init__()
        self._cfg = cfg
        self._prompt_action = prompt_action
        self.mcts: MCTS

    def get_action(self, env: MultiAgentMctsEnv) -> int:
        self.mcts = MCTS(env, self._cfg)
        action = self.mcts.get_action()
        if self._prompt_action:
            input("Opponent's turn, press enter to continue")
        return action

    def __str__(self) -> str:
        return self.__class__.__name__ + "|" + str(self._cfg)
