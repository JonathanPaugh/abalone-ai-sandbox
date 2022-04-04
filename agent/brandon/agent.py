from threading import Thread

from agent.base import BaseAgent
from agent.brandon.search import Search
from core.board import Board
from core.color import Color
from ui.model.heuristic_type import HeuristicType


def agent_thread(search, board, color, on_find, on_complete):
    search.start(board, color, on_find)
    on_complete()


class BrandonAgent(BaseAgent):

    def __init__(self):
        self._search = Search()
        self._thread = None

    @property
    def is_searching(self):
        return self._thread is not None and self._thread.is_alive()

    def start(self, board: Board, player: Color, on_find: callable, on_complete: callable):
        thread = Thread(target=agent_thread, args=(self._search, board, player, on_find, on_complete))
        thread.daemon = True
        thread.start()
        self._thread = thread

    def stop(self):
        self._search.stop()

    def toggle_paused(self):
        self._search.toggle_paused()

    def set_heuristic_type(self, heuristic_type: HeuristicType):
        self._search.heuristic = heuristic_type
