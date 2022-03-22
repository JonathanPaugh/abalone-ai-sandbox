from __future__ import annotations
from typing import TYPE_CHECKING

from agent.agent import Agent
from ui.agent_thread import AgentThread

if TYPE_CHECKING:
    from core.board import Board
    from core.color import Color
    from core.move import Move


class AgentOperator:
    def __init__(self):
        self.agent = Agent()
        self.thread = None

    def search(self, board: Board, player: Color, on_find: callable):
        self._launch_thread(board, player, lambda move: self._on_search_find(move, on_find))

    def stop(self):
        if self.thread:
            self.thread.stop()

        self.thread = None

    def _on_search_find(self, move: Move, on_find: callable):
        if self.thread:
            on_find(move)

    def _on_search_complete(self, on_timeout: callable):
        self.thread.stop()
        on_timeout(self.best_move)

    def _launch_thread(self, board: Board, player: Color, on_find_move: callable):
        if self.thread and self.thread.is_alive():
            self.thread.stop()
            raise Exception("Agent thread attempted to start while previous thread still alive")

        self.thread = AgentThread(self.agent, board, player, on_find_move)
        self.thread.start()
