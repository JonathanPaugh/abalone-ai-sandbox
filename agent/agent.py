from __future__ import annotations
from typing import TYPE_CHECKING

from agent.agent_thread import AgentThread
from agent.heuristics.heuristic_type import HeuristicType
from agent.search import Search

if TYPE_CHECKING:
    from core.board import Board
    from core.color import Color


class Agent:
    def __init__(self):
        self._search = Search()
        self._thread = None

    def search(self, board: Board, player: Color, on_find: callable, on_complete: callable):
        self._launch_thread(board, player, on_find, on_complete)

    def set_heuristic_type(self, heuristic_type: HeuristicType):
        self._search.set_heuristic_type(heuristic_type)

    def stop(self):
        if self._thread and self._thread.running:
            self._thread.stop()
        self._thread = None

    def _launch_thread(self, board: Board, player: Color, on_find_move: callable, on_complete: callable):
        if self._thread and self._thread.is_alive():
            self._thread.stop()
            raise Exception("Agent thread attempted to start while previous thread still alive")

        self._thread = AgentThread(self._search, board, player, on_find_move, on_complete)
        self._thread.start()
