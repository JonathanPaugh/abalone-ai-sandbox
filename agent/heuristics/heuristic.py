from math import inf
from core.board import Board
from core.color import Color
from core.constants import BOARD_SIZE, WIN_SCORE
from core.hex import Hex
from lib.clamp import clamp_01, clamp
from lib.remap import remap_01, remap


class Heuristic:
    BOARD_CENTER = Hex(BOARD_SIZE - 1, BOARD_SIZE - 1)
    MAX_MANHATTAN_DISTANCE = BOARD_SIZE - 1

    # Base Weights #
    WEIGHT_SCORE = 0.45
    WEIGHT_OPPONENT_SCORE = 0.45
    WEIGHT_MANHATTAN = 0.04
    WEIGHT_OPPONENT_MANHATTAN = 0.05
    WEIGHT_ADJACENCY = 0.005
    WEIGHT_OPPONENT_ADJACENCY = 0.005

    # Normalized Weights #
    WEIGHT_NORMALIZED_SCORE = 0.275
    WEIGHT_NORMALIZED_OPPONENT_SCORE = 0.30
    WEIGHT_NORMALIZED_MANHATTAN = 0.10
    WEIGHT_NORMALIZED_OPPONENT_MANHATTAN = 0.15
    WEIGHT_NORMALIZED_ADJACENCY = 0.10
    WEIGHT_NORMALIZED_OPPONENT_ADJACENCY = 0.075

    # Dynamic Settings #
    MIN_MARBLE_COUNT = 9
    MAX_MARBLE_COUNT = 14

    DYNAMIC_TURN_MAX = 20
    _dynamic_turn_count = 0

    @classmethod
    def increment_dynamic_turn_count(cls):
        cls._dynamic_turn_count = clamp(0, cls.DYNAMIC_TURN_MAX, cls._dynamic_turn_count + 1)

    @classmethod
    def weighted(cls, board: Board, player: Color) -> float:
        _, _, \
        score, score_opponent, \
        manhattan_score, manhattan_opponent_score, \
        adjacency_score, adjacency_opponent_score = cls._composite(board, player)

        return cls.WEIGHT_SCORE * score \
               + cls.WEIGHT_OPPONENT_SCORE * score_opponent \
               + cls.WEIGHT_MANHATTAN * manhattan_score \
               + cls.WEIGHT_OPPONENT_MANHATTAN * manhattan_opponent_score \
               + cls.WEIGHT_ADJACENCY * adjacency_score \
               + cls.WEIGHT_OPPONENT_ADJACENCY * adjacency_opponent_score

    @classmethod
    def weighted_normalized(cls, board: Board, player: Color) -> float:
        score, score_opponent, \
        manhattan_score, manhattan_opponent_score, \
        adjacency_score, adjacency_opponent_score = cls._composite_normalized(board, player)

        return cls.WEIGHT_NORMALIZED_SCORE * score \
               + cls.WEIGHT_NORMALIZED_OPPONENT_SCORE * score_opponent \
               + cls.WEIGHT_NORMALIZED_MANHATTAN * manhattan_score \
               + cls.WEIGHT_NORMALIZED_OPPONENT_MANHATTAN * manhattan_opponent_score \
               + cls.WEIGHT_NORMALIZED_ADJACENCY * adjacency_score \
               + cls.WEIGHT_NORMALIZED_OPPONENT_ADJACENCY * adjacency_opponent_score

    @classmethod
    def dynamic(cls, board: Board, player: Color) -> float:
        score, score_opponent, \
        manhattan_score, manhattan_opponent_score, \
        adjacency_score, adjacency_opponent_score = cls._composite_normalized(board, player)

        weight_initial_score = cls.WEIGHT_SCORE / 2
        weight_final_score = cls.WEIGHT_SCORE

        weight_initial_normalized_manhattan = cls.WEIGHT_NORMALIZED_MANHATTAN + weight_initial_score
        weight_final_normalized_manhattan = 0

        weight_initial_normalized_opponent_manhattan = cls.WEIGHT_NORMALIZED_OPPONENT_MANHATTAN
        weight_final_normalized_opponent_manhattan = cls.WEIGHT_NORMALIZED_OPPONENT_MANHATTAN \
                                                     + cls.WEIGHT_NORMALIZED_MANHATTAN

        weight_normalized_score = remap(cls._dynamic_turn_count, 0, cls.DYNAMIC_TURN_MAX,
                                        weight_initial_score,
                                        weight_final_score)

        weight_normalized_manhattan = remap(cls._dynamic_turn_count, 0, cls.DYNAMIC_TURN_MAX,
                                            weight_initial_normalized_manhattan,
                                            weight_final_normalized_manhattan)

        weight_normalized_opponent_manhattan = remap(cls._dynamic_turn_count, 0, cls.DYNAMIC_TURN_MAX,
                                                     weight_initial_normalized_opponent_manhattan,
                                                     weight_final_normalized_opponent_manhattan)

        return weight_normalized_score * score \
               + cls.WEIGHT_NORMALIZED_OPPONENT_SCORE * score_opponent \
               + weight_normalized_manhattan * manhattan_score \
               + weight_normalized_opponent_manhattan * manhattan_opponent_score \
               + cls.WEIGHT_NORMALIZED_ADJACENCY * adjacency_score \
               + cls.WEIGHT_NORMALIZED_OPPONENT_ADJACENCY * adjacency_opponent_score

    @classmethod
    def _score(cls, board: Board, player: Color) -> int:
        score = board.get_score(player)
        if score >= WIN_SCORE:
            return inf
        return score

    @classmethod
    def _score_opponent(cls, board: Board, player: Color) -> int:
        score = board.get_score(Color.next(player))
        if score >= WIN_SCORE:
            return -inf
        return WIN_SCORE - score

    @classmethod
    def _score_optimized(cls, board: Board, player: Color, player_count: int, opponent_count: int) -> int:
        player_score, opponent_score = board.get_scores_optimized(player, player_count, opponent_count)

        if player_score >= WIN_SCORE:
            player_score = inf
            
        if opponent_score >= WIN_SCORE:
            opponent_score = -inf
        else:
            opponent_score = WIN_SCORE - opponent_score

        return player_score, opponent_score

    @classmethod
    def _manhattan(cls, board: Board, player: Color) -> int:
        score = 0
        for cell, color in board.enumerate():
            if color is player:
                score += cls.MAX_MANHATTAN_DISTANCE - cell.manhattan(cls.BOARD_CENTER)
        return score

    @classmethod
    def _manhattan_opponent(cls, board: Board, player: Color) -> int:
        score = 0
        for cell, color in board.enumerate():
            if color is Color.next(player):
                score += cell.manhattan(cls.BOARD_CENTER)
        return score

    @classmethod
    def _adjacency(cls, board: Board, player: Color) -> int:
        score = 0
        for cell, color in board.enumerate():
            if color is not player:
                continue

            for neighbour in cell.neighbors():
                if board.cell_in_bounds(neighbour) and board[neighbour] == player:
                    score += 1

        return score

    @classmethod
    def _adjacency_opponent(cls, board: Board, player: Color) -> int:
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
    def _score_normalized(cls, score: int) -> float:
        floor = 0
        ceiling = WIN_SCORE
        if score >= inf:
            return inf
        return remap_01(score, floor, ceiling)

    @classmethod
    def _score_opponent_normalized(cls, score: int) -> float:
        floor = 0
        ceiling = WIN_SCORE
        if score <= -inf:
            return -inf
        return remap_01(score, floor, ceiling)

    @classmethod
    def _manhattan_normalized(cls, score: int, marble_count: int) -> float:
        floor = 0
        ceiling_min = 26
        ceiling_max = 36

        ceiling = cls._map_limit_by_marble_count(marble_count, ceiling_min, ceiling_max)
        return clamp_01(remap_01(score, floor, ceiling))

    @classmethod
    def _manhattan_opponent_normalized(cls, score: int, marble_count: int) -> float:
        floor_min = 10
        floor_max = 20
        ceiling_min = 36
        ceiling_max = 56

        floor = cls._map_limit_by_marble_count(marble_count, floor_min, floor_max)
        ceiling = cls._map_limit_by_marble_count(marble_count, ceiling_min, ceiling_max)

        return clamp_01(remap_01(score, floor, ceiling))

    @classmethod
    def _adjacency_normalized(cls, score: int, marble_count: int) -> float:
        floor = 0
        ceiling_min = 32
        ceiling_max = 56

        ceiling = cls._map_limit_by_marble_count(marble_count, ceiling_min, ceiling_max)

        return clamp_01(remap_01(score, floor, ceiling))

    @classmethod
    def _adjacency_opponent_normalized(cls, score: int, marble_count: int) -> float:
        floor_min = 22
        floor_max = 28
        ceiling_min = 54
        ceiling_max = 84

        floor = cls._map_limit_by_marble_count(marble_count, floor_min, floor_max)
        ceiling = cls._map_limit_by_marble_count(marble_count, ceiling_min, ceiling_max)

        return clamp_01(remap_01(score, floor, ceiling))

    @classmethod
    def _composite(cls, board: Board, player: Color):
        manhattan_score = 0
        manhattan_opponent_score = 0
        adjacency_score = 0
        adjacency_opponent_score = 0

        player_count, opponent_count = board.get_marble_counts_optimized(player)
        score, opponent_score = cls._score_optimized(board, player, player_count, opponent_count)

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
               score, opponent_score, \
               manhattan_score, manhattan_opponent_score, \
               adjacency_score, adjacency_opponent_score

    @classmethod
    def _composite_normalized(cls, board: Board, player: Color):
        player_count, opponent_count, \
        score, score_opponent, \
        manhattan_score, manhattan_opponent_score, \
        adjacency_score, adjacency_opponent_score = cls._composite(board, player)

        return cls._score_normalized(score), \
               cls._score_opponent_normalized(score_opponent), \
               cls._manhattan_normalized(manhattan_score, player_count), \
               cls._manhattan_opponent_normalized(manhattan_opponent_score, opponent_count), \
               cls._adjacency_normalized(adjacency_score, player_count), \
               cls._adjacency_opponent_normalized(adjacency_opponent_score, opponent_count)

    @classmethod
    def _map_limit_by_marble_count(cls, count: int, min: int, max: int):
        return remap(count, cls.MIN_MARBLE_COUNT, cls.MAX_MARBLE_COUNT, min, max)
