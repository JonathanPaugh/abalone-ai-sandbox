from copy import deepcopy
from core.board import Board
from core.color import Color
from agent.state_generator import StateGenerator


class Search:

    def __init__(self):
        self.heuristic = None
        self._stopped = False
        self._paused = False

    def start(self, board: Board, color: Color, on_find: callable):
        moves = StateGenerator.enumerate_board(board, color)
        moves.sort(key=lambda move: (
            move_board := deepcopy(board),
            move_board.apply_move(move),
            self.heuristic.call(move_board, color),
        )[-1])
        best_move = moves[-1]
        on_find(best_move)

    def stop(self):
        self._stopped = True

    def toggle_paused(self):
        self._paused = not self._paused
