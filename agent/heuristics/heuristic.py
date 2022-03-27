from math import inf
from numbers import Number

from core.board import Board
from core.color import Color
from core.constants import BOARD_SIZE, WIN_SCORE
from core.hex import Hex
from lib.remap import remap_01


class Heuristic:
    MAX_MANHATTAN_DISTANCE = BOARD_SIZE - 1
    BOARD_CENTER = Hex(BOARD_SIZE - 1, BOARD_SIZE - 1)

    @classmethod
    def main(cls, board: Board, player: Color) -> Number:
        return cls.weighted_normalized(board, player)

    @classmethod
    def weighted(cls, board: Board, player: Color) -> float:
        score_weight = 0.45
        score_opponent_weight = 0.45
        manhattan_weight = 0.04
        manhattan_opponent_weight = 0.05
        adjacency_weight = 0.005
        adjacency_opponent_weight = 0.005

        return score_weight * cls.score(board, player) \
            + score_opponent_weight * cls.score_opponent(board, player) \
            + manhattan_weight * cls.manhattan(board, player) \
            + manhattan_opponent_weight * cls.manhattan_opponent(board, player) \
            + adjacency_weight * cls.adjacency(board, player) \
            + adjacency_opponent_weight * cls.adjacency_opponent(board, player)

    @classmethod
    def weighted_normalized(cls, board: Board, player: Color) -> float:
        score_weight = 0.20
        score_opponent_weight = 0.25
        manhattan_weight = 0.15
        manhattan_opponent_weight = 0.175
        adjacency_weight = 0.125
        adjacency_opponent_weight = 0.10

        return score_weight * cls.score_normalized(board, player) \
            + score_opponent_weight * cls.score_opponent_normalized(board, player) \
            + manhattan_weight * cls.manhattan_normalized(board, player) \
            + manhattan_opponent_weight * cls.manhattan_opponent_normalized(board, player) \
            + adjacency_weight * cls.adjacency_normalized(board, player) \
            + adjacency_opponent_weight * cls.adjacency_opponent_normalized(board, player)

    @classmethod
    def score(cls, board: Board, player: Color) -> int:
        score = board.get_score(player)
        if score >= WIN_SCORE:
            return inf
        return score

    @classmethod
    def score_opponent(cls, board: Board, player: Color) -> int:
        score = board.get_score(Color.next(player))
        if score >= WIN_SCORE:
            return -inf
        return WIN_SCORE - score

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

    @classmethod
    def score_normalized(cls, board: Board, player: Color) -> float:
        floor = 0
        ceiling = WIN_SCORE
        score = cls.score(board, player)
        if score >= inf:
            return inf
        return remap_01(score, floor, ceiling)

    @classmethod
    def score_opponent_normalized(cls, board: Board, player: Color) -> float:
        floor = 0
        ceiling = WIN_SCORE
        score = cls.score_opponent(board, player)
        if score <= -inf:
            return -inf
        return remap_01(score, floor, ceiling)

    @classmethod
    def manhattan_normalized(cls, board: Board, player: Color) -> float:
        floor = 0
        ceiling = 36
        return remap_01(cls.manhattan(board, player), floor, ceiling)

    @classmethod
    def manhattan_opponent_normalized(cls, board: Board, player: Color) -> float:
        floor = 20
        ceiling = 56
        return remap_01(cls.manhattan_opponent(board, player), floor, ceiling)

    @classmethod
    def adjacency_normalized(cls, board: Board, player: Color) -> float:
        floor = 0
        ceiling = 56
        return remap_01(cls.adjacency(board, player), floor, ceiling)

    @classmethod
    def adjacency_opponent_normalized(cls, board: Board, player: Color) -> float:
        floor = 28
        ceiling = 84
        return remap_01(cls.adjacency_opponent(board, player), floor, ceiling)


