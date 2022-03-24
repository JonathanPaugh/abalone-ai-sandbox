from math import inf
from numbers import Number

from core.board import Board
from core.color import Color
from core.constants import BOARD_SIZE, WIN_SCORE
from core.hex import Hex


class Heuristics:
    MAX_MANHATTAN_DISTANCE = BOARD_SIZE - 1
    BOARD_CENTER = Hex(BOARD_SIZE - 1, BOARD_SIZE - 1)

    @classmethod
    def main(cls, board: Board, player: Color) -> Number:
        return cls.weighted(board, player)

    @classmethod
    def weighted(cls, board: Board, player: Color) -> float:
        SCORE_WIEGHT = 0.9
        MANHATTAN_WIEGHT = 0.03
        MANHATTAN_OPPONENT_WIEGHT = 0.05
        ADJACENCY_WIEGHT = 0.01
        ADJACENCY_OPPONENT_WIEGHT = 0.01

        return SCORE_WIEGHT * cls.score(board, player) \
               + MANHATTAN_WIEGHT * cls.manhattan(board, player) \
               + MANHATTAN_OPPONENT_WIEGHT * cls.manhattan_opponent(board, player) \
               + ADJACENCY_WIEGHT * cls.adjacency(board, player) \
               + ADJACENCY_OPPONENT_WIEGHT * cls.adjacency_opponent(board, player)

    @classmethod
    def manhattan(cls, board: Board, player: Color) -> int:
        score = 0
        for cell, color in board.enumerate():
            if color is player:
                score += cls.MAX_MANHATTAN_DISTANCE - cell.manhattan(cls.BOARD_CENTER)
        return score

    @classmethod
    def manhattan_opponent(cls, board: Board, player: Color) -> int:
        score = 0
        for cell, color in board.enumerate():
            if color is Color.next(player):
                score += cell.manhattan(cls.BOARD_CENTER)
        return score

    @classmethod
    def score(cls, board: Board, player: Color) -> int:
        score = board.get_score(player)
        if score >= WIN_SCORE:
            return inf
        return score

    @classmethod
    def adjacency(cls, board: Board, player: Color) -> int:
        score = 0
        for cell, color in board.enumerate():
            if color is not player:
                continue

            for neighbour in cell.neighbors():
                if board.cell_in_bounds(neighbour) and board[neighbour] == player:
                    score += 1

        return score

    @classmethod
    def adjacency_opponent(cls, board: Board, player: Color) -> int:
        return 0
