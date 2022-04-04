from copy import deepcopy
from threading import Thread

from agent.ponderer import PonderingAgent
from agent.brandon.search import Search
from agent.state_generator import StateGenerator
from core.board import Board
from core.color import Color
from ui.model.heuristic_type import HeuristicType


def search_worker(search, board, color, on_find, on_complete):
    search.start(board, color, on_find)
    on_complete()

def ponder_worker(search, board, color, on_find, on_complete):
    NUM_PREDICTIONS = 2

    opponent_moves = StateGenerator.enumerate_board(board, color)
    opponent_moves.sort(key=lambda move: (
        move_board := deepcopy(board),
        move_board.apply_move(move),
        search.heuristic.call(move_board, color)
    )[-1], reverse=True)
    opponent_moves = opponent_moves[:NUM_PREDICTIONS]

    for opponent_move in opponent_moves:
        agent_board = deepcopy(board)
        agent_board.apply_move(opponent_move)

        best_move = None
        def set_best_move(move):
            nonlocal best_move
            best_move = move

        exhausted = search.start(agent_board, Color.next(color), set_best_move)
        if exhausted and best_move:
            print("set refutation for", opponent_move, "->", best_move)
            on_find(opponent_move, best_move)

        if search.stopped:
            break

    if on_complete:
        on_complete()


class BrandonPonderer(PonderingAgent):

    def __init__(self):
        self._search = Search()
        self._search_mode = None
        self._thread = None

    @property
    def is_searching(self):
        return self._thread is not None and self._thread.is_alive()

    def _create_normal_search_thread(self, board: Board, player: Color,
                                     on_find: callable, on_complete: callable):
        return Thread(target=search_worker, args=(
            self._search,
            board,
            player,
            on_find,
            on_complete
        ))

    def _create_ponder_search_thread(self, board: Board, player: Color,
                                     on_find: callable, on_complete: callable):
        return Thread(target=ponder_worker, args=(
            self._search,
            board,
            player,
            on_find,
            on_complete
        ))

    def _start_search(self, thread):
        thread.daemon = True
        thread.start()
        self._thread = thread

    def start(self, board: Board, player: Color, on_find: callable, on_complete: callable):
        thread = self._create_normal_search_thread(board, player, on_find, on_complete)
        self._search_mode = self.SearchMode.NORMAL_SEARCH
        self._start_search(thread)

    def ponder(self, board: Board, player: Color, on_find: callable, on_complete: callable = None):
        thread = self._create_ponder_search_thread(board, player, on_find, on_complete)
        self._search_mode = self.SearchMode.PONDER_SEARCH
        self._start_search(thread)

    def stop(self):
        self._search.stop()
        self._search_mode = None

    def toggle_paused(self):
        self._search.toggle_paused()

    def set_heuristic_type(self, heuristic_type: HeuristicType):
        self._search.heuristic = heuristic_type
