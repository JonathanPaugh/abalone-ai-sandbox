from math import inf
from time import sleep
from copy import deepcopy
from core.board import Board
from core.color import Color
from agent.state_generator import StateGenerator
from ui.constants import FPS


class Search:

    def __init__(self):
        self.heuristic = None
        self._stopped = False
        self._paused = False

    def start(self, board: Board, color: Color, on_find: callable):
        self._stopped = False
        try:
            self._search(board, color, on_find)
        except StopIteration:
            pass

    def stop(self):
        self._paused = False
        self._stopped = True

    def toggle_paused(self):
        self._paused = not self._paused

    def _search(self, board: Board, color: Color, on_find: callable):
        moves = StateGenerator.enumerate_board(board, color)
        alpha = -inf

        for move in moves:
            self._handle_interrupts()
            move_board = deepcopy(board)
            move_board.apply_move(move)
            move_score = -self._negamax(move_board, color, 1, -inf, -alpha, -1)
            if move_score > alpha:
                alpha = move_score
                on_find(move)

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

            move_score = -self._negamax(board, color, depth - 1, -beta, -alpha, -perspective)
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
