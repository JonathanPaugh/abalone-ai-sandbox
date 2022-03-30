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
        """
        Start the search using a board and a player as a starting state.
        :param on_find: A function that gets called everytime a better move is found.
        :param on_complete: A function that gets called when a search runs to exhaustion without interruption.
        """
        self._launch_thread(board, player, on_find, on_complete)

    def set_heuristic_type(self, heuristic_type: HeuristicType):
        """
        Sets the heuristic type to be used by the search.
        :param heuristic_type: The heuristic type.
        """
        self._search.set_heuristic_type(heuristic_type)

    def stop(self):
        """
        Force the search to stop.
        """
        if self._thread and self._thread.running:
            self._thread.stop()
        self._thread = None

    def _launch_thread(self, board: Board, player: Color, on_find: callable, on_complete: callable):
        """
        Launches a thread to run a search.
        :param on_find: A function that gets called everytime a better move is found.
        :param on_complete: A function that gets called when a search runs to exhaustion without interruption.
        """
        if self._thread and self._thread.is_alive():
            self._thread.stop()
            raise Exception("Agent thread attempted to start while previous thread still alive")

        self._thread = AgentThread(self._search, board, player, on_find, on_complete)
        self._thread.start()
