from math import inf
from core.board import Board
from core.color import Color
from core.constants import BOARD_SIZE, WIN_SCORE
from core.hex import Hex
from lib.clamp import clamp_01
from lib.remap import remap_01, remap


class Heuristic:
    MIN_MARBLE_COUNT = 9
    MAX_MARBLE_COUNT = 14
    MAX_MANHATTAN_DISTANCE = BOARD_SIZE - 1
    BOARD_CENTER = Hex(BOARD_SIZE - 1, BOARD_SIZE - 1)

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
        score_weight = 0.25
        score_opponent_weight = 0.30
        manhattan_weight = 0.125
        manhattan_opponent_weight = 0.15
        adjacency_weight = 0.10
        adjacency_opponent_weight = 0.075

        score, score_opponent, \
            manhattan_score, manhattan_opponent_score, \
            adjacency_score, adjacency_opponent_score = cls.composite_normalized(board, player)

        return score_weight * score \
            + score_opponent_weight * score_opponent \
            + manhattan_weight * manhattan_score \
            + manhattan_opponent_weight * manhattan_opponent_score \
            + adjacency_weight * adjacency_score \
            + adjacency_opponent_weight * adjacency_opponent_score

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
    def score_normalized(cls, score: int) -> float:
        floor = 0
        ceiling = WIN_SCORE
        if score >= inf:
            return inf
        return remap_01(score, floor, ceiling)

    @classmethod
    def score_opponent_normalized(cls, score: int) -> float:
        floor = 0
        ceiling = WIN_SCORE
        if score <= -inf:
            return -inf
        return remap_01(score, floor, ceiling)

    @classmethod
    def manhattan_normalized(cls, score: int, marble_count: int) -> float:
        floor = 0
        ceiling_min = 26
        ceiling_max = 36

        ceiling = cls._map_limit_by_marble_count(marble_count, ceiling_min, ceiling_max)
        return clamp_01(remap_01(score, floor, ceiling))

    @classmethod
    def manhattan_opponent_normalized(cls, score: int, marble_count: int) -> float:
        floor_min = 10
        floor_max = 20
        ceiling_min = 36
        ceiling_max = 56

        floor = cls._map_limit_by_marble_count(marble_count, floor_min, floor_max)
        ceiling = cls._map_limit_by_marble_count(marble_count, ceiling_min, ceiling_max)

        return clamp_01(remap_01(score, floor, ceiling))

    @classmethod
    def adjacency_normalized(cls, score: int, marble_count: int) -> float:
        floor = 0
        ceiling_min = 32
        ceiling_max = 56

        ceiling = cls._map_limit_by_marble_count(marble_count, ceiling_min, ceiling_max)

        return clamp_01(remap_01(score, floor, ceiling))

    @classmethod
    def adjacency_opponent_normalized(cls, score: int, marble_count: int) -> float:
        floor_min = 22
        floor_max = 28
        ceiling_min = 54
        ceiling_max = 84

        floor = cls._map_limit_by_marble_count(marble_count, floor_min, floor_max)
        ceiling = cls._map_limit_by_marble_count(marble_count, ceiling_min, ceiling_max)

        return clamp_01(remap_01(score, floor, ceiling))

    @classmethod
    def composite(cls, board: Board, player: Color):
        manhattan_score = 0
        manhattan_opponent_score = 0
        adjacency_score = 0
        adjacency_opponent_score = 0

        player_count = board.get_marble_count(player)
        opponent_count = board.get_marble_count(Color.next(player))

        for cell, color in board.enumerate():
            for neighbour in cell.neighbors():
                if color is player:
                    if board.cell_in_bounds(neighbour) and board[neighbour] == player:
                        adjacency_score += 1
                elif color is Color.next(player):
                    if not board.cell_in_bounds(neighbour):
                        adjacency_opponent_score += 1
                    elif board[neighbour] != Color.next(player):
                        adjacency_opponent_score += 1

            if color is player:
                manhattan_score += cls.MAX_MANHATTAN_DISTANCE - cell.manhattan(cls.BOARD_CENTER)
            elif color is Color.next(player):
                manhattan_opponent_score += cell.manhattan(cls.BOARD_CENTER)
            else:
                pass

        return player_count, opponent_count, \
            cls.score(board, player), cls.score_opponent(board, player), \
            manhattan_score, manhattan_opponent_score, \
            adjacency_score, adjacency_opponent_score

    @classmethod
    def composite_normalized(cls, board: Board, player: Color):
        player_count, opponent_count, \
            score, score_opponent, \
            manhattan_score, manhattan_opponent_score, \
            adjacency_score, adjacency_opponent_score = cls.composite(board, player)

        return cls.score_normalized(score), \
            cls.score_opponent_normalized(score_opponent), \
            cls.manhattan_normalized(manhattan_score, player_count), \
            cls.manhattan_opponent_normalized(manhattan_opponent_score, opponent_count), \
            cls.adjacency_normalized(adjacency_score, player_count), \
            cls.adjacency_opponent_normalized(adjacency_opponent_score, opponent_count)

    @classmethod
    def _map_limit_by_marble_count(cls, count: int, min: int, max: int):
        return remap(count, cls.MIN_MARBLE_COUNT, cls.MAX_MARBLE_COUNT, min, max)
