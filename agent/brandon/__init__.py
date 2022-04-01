from time import sleep
from threading import Thread
from multiprocessing import Queue, Process
from multiprocessing.managers import BaseManager
from queue import Empty

from agent import BaseAgent
from agent.brandon.search import Search
from core.board import Board
from core.color import Color
from ui.model.heuristic_type import HeuristicType
from ui.constants import FPS


class ConsumerThread(Thread):

    def __init__(self, queue, on_find, on_complete):
        super().__init__()
        self._queue = queue
        self._on_find = on_find
        self._on_complete = on_complete

    def run(self):
        queue = self._queue
        on_find = self._on_find
        on_complete = self._on_complete

        done_search = False
        while not done_search:
            try:
                new_move, done_search = queue.get(block=False)
            except Empty:
                new_move, done_search = None, False

            if new_move:
                on_find(new_move)

            if done_search:
                on_complete()

            sleep(1 / FPS)


class SearchProcess(Process):

    def __init__(self, queue, search, board, color):
        super().__init__()
        self._queue = queue
        self._search = search
        self._board = board
        self._color = color

    def _on_find(self, move):
        self._queue.put((move, False))

    def run(self):
        queue = self._queue
        search = self._search
        board = self._board
        color = self._color

        search.start(board, color, self._on_find)
        queue.put((None, True))


class SearchManager(BaseManager): pass
SearchManager.register("Search", Search)


class BrandonAgent(BaseAgent):

    def __init__(self):
        manager = SearchManager()
        manager.start()
        # pylint: disable=no-member
        self._search = manager.Search()
        self._process = None
        self._queue = None

    def start(self, board: Board, player: Color, on_find: callable, on_complete: callable):
        queue = Queue()
        self._queue = queue

        thread = ConsumerThread(queue, on_find, on_complete)
        thread.daemon = True
        thread.start()
        self._thread = thread

        process = SearchProcess(queue, self._search, board, player)
        process.daemon = True
        process.start()
        self._process = process

    def stop(self):
        pass

    def toggle_paused(self):
        pass

    def set_heuristic_type(self, heuristic_type: HeuristicType):
        pass
