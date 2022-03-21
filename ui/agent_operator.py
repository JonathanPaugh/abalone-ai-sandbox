from threading import Timer

from agent.agent import Agent
from ui.agent_thread import AgentThread


class AgentOperator:
    def __init__(self):
        self.agent = Agent()
        self.thread = None

    def search(self, board, player, on_find):
        self._launch_thread(board, player, lambda move: self._on_search_find(move, on_find))

    def stop(self):
        if self.thread:
            self.thread.stop()

        self.thread = None

    def _on_search_find(self, move, on_find):
        if self.thread:
            on_find(move)

    def _on_search_complete(self, on_timeout):
        self.thread.stop()
        on_timeout(self.best_move)

    def _launch_thread(self, board, player, on_find_move):
        if self.thread and self.thread.is_alive():
            self.thread.stop()
            raise Exception("Agent thread attempted to start while previous thread still alive")

        self.thread = AgentThread(self.agent, board, player, on_find_move)
        self.thread.start()
