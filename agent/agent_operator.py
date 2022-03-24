from __future__ import annotations
from typing import TYPE_CHECKING

from agent.agent import Agent
from agent.agent_thread import AgentThread

if TYPE_CHECKING:
    from core.board import Board
    from core.color import Color


class AgentOperator:
    def __init__(self):
        self.agent = Agent()
        self.thread = None

    def search(self, board: Board, player: Color, on_find: callable):
        self._launch_thread(board, player, on_find)

    def stop(self):
        if self.thread:
            self.thread.stop()
        self.thread = None

    def _launch_thread(self, board: Board, player: Color, on_find_move: callable):
        if self.thread and self.thread.is_alive():
            self.thread.stop()
            raise Exception("Agent thread attempted to start while previous thread still alive")

        self.thread = AgentThread(self.agent, board, player, on_find_move)
        self.thread.start()
