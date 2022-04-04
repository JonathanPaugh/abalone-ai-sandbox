from math import inf
from time import sleep
from copy import deepcopy
from core.board import Board
from core.color import Color
from agent.state_generator import StateGenerator
from ui.constants import FPS
from ui.debug import Debug


class Search:
    """
    An interface around Abalone search logic.
    """

    @staticmethod
    def _estimate_move_score(board, move):
        WEIGHT_SUMITO = 10 # consider sumitos first
        return (len(move.get_cells())
            + WEIGHT_SUMITO * move.is_sumito(board))

    @classmethod
    def _order_moves(cls, board, moves):
        return sorted(moves, key=lambda move: cls._estimate_move_score(board, move), reverse=True)

    def __init__(self):
        self.heuristic = None
        self._stopped = False
        self._paused = False

    @property
    def stopped(self):
        return self._stopped

    def start(self, board: Board, color: Color, on_find: callable):
        """
        Starts the search.
        """
        self._stopped = False
        try:
            self._search(board, color, on_find)
        except StopIteration:
            pass

    def stop(self):
        """
        Stops the search.
        """
        self._paused = False
        self._stopped = True

    def toggle_paused(self):
        """
        Pauses or unpauses the search.
        """
        self._paused = not self._paused

    def _search(self, board: Board, color: Color, on_find: callable):
        moves = StateGenerator.enumerate_board(board, color)
        moves = self._order_moves(board, moves)
        alpha = -inf

        for move in moves:
            self._handle_interrupts()
            move_board = deepcopy(board)
            move_board.apply_move(move)

            move_score = -self._negamax(move_board, color, 1, -inf, -alpha, -1)
            if move_score > alpha:
                alpha = move_score
                on_find(move)
                Debug.log(f"new best move {move}/{move_score:.2f}")

    def _negamax(self, board, color, depth, alpha, beta, perspective):
        self._handle_interrupts()

        if depth == 0:
            return self.heuristic.call(board, color) * perspective

        best_score = -inf
        true_color = color if perspective == 1 else Color.next(color)

        moves = StateGenerator.enumerate_board(board, true_color)
        for move in moves:
            move_board = deepcopy(board)
            move_board.apply_move(move)

            move_score = -self._negamax(move_board, color, depth - 1, -beta, -alpha, -perspective)
            if move_score > best_score:
                best_score = move_score

            alpha = max(alpha, best_score)
            if alpha >= beta:
                break

        return best_score

    def _handle_interrupts(self):
        while self._paused:
            sleep(1 / FPS)

        if self._stopped:
            raise StopIteration
