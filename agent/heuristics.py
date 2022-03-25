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
        score_weight = 0.9
        manhattan_weight = 0.03
        manhattan_opponent_weight = 0.05
        adjacency_weight = 0.01
        adjacency_opponent_weight = 0.01

        return score_weight * cls.score(board, player) \
               + manhattan_weight * cls.manhattan(board, player) \
               + manhattan_opponent_weight * cls.manhattan_opponent(board, player) \
               + adjacency_weight * cls.adjacency(board, player) \
               + adjacency_opponent_weight * cls.adjacency_opponent(board, player)

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
        score = 0
        for cell, color in board.enumerate():
            if color is not Color.next(player):
                continue

            for neighbour in cell.neighbors():
                if not board.cell_in_bounds(neighbour):
                    score += 1
                elif board[neighbour] != Color.next(player):
                    score += 1

        return score
