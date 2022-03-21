from threading import Timer

from agent.agent import Agent
from ui.agent_thread import AgentThread


class AgentOperator:
    def __init__(self):
        self.agent = Agent()
        self.thread = None
        self.best_move = None

    def search(self, board, player, timeout, on_timeout):
        self._launch_thread(board, player)
        Timer(timeout, lambda: self._on_search_complete(on_timeout)).start()

    def _on_search_complete(self, on_timeout):
        self.thread.stop()
        on_timeout(self.best_move)

    def _launch_thread(self, board, player):
        if self.thread and self.thread.is_alive():
            self.thread.stop()
            raise("Agent thread attempted to start while previous thread still alive")

        self.thread = AgentThread(self.agent, board, player, self._update_best_move)
        self.thread.start()

    def _update_best_move(self, move):
        self.best_move = move
