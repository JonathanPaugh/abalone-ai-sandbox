from math import inf
from numbers import Number

from core.board import Board
from core.color import Color
from core.constants import BOARD_SIZE, WIN_SCORE
from core.hex import Hex
from lib.clamp import clamp_01, clamp
from lib.remap import remap_01, remap
from ui import debug
from ui.debug import DebugType, Debug


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

    DYNAMIC_TURN_MAX = 30
    _get_turn_count = None

    @classmethod
    def set_turn_count_handler(cls, get_turn_count):
        """
        Sets the turn count handler for dynamic heuristics.
        """
        cls._get_turn_count = lambda: clamp(0, cls.DYNAMIC_TURN_MAX, get_turn_count())

    @classmethod
    def weighted(cls, board: Board, player: Color) -> float:
        """
        Calculates a heuristic value using 6 base heuristics and individually weighting them.
        :return: The heuristic value.
        """
        score, score_opponent, \
        manhattan_score, manhattan_opponent_score, \
        adjacency_score, adjacency_opponent_score, \
        _, _ = cls._composite(board, player)

        return cls.WEIGHT_SCORE * score \
               + cls.WEIGHT_OPPONENT_SCORE * score_opponent \
               + cls.WEIGHT_MANHATTAN * manhattan_score \
               + cls.WEIGHT_OPPONENT_MANHATTAN * manhattan_opponent_score \
               + cls.WEIGHT_ADJACENCY * adjacency_score \
               + cls.WEIGHT_OPPONENT_ADJACENCY * adjacency_opponent_score

    @classmethod
    def weighted_normalized(cls, board: Board, player: Color) -> float:
        """
        Calculates a heuristic value using 6 base heuristics and converting them to a number between 0.0 and 1.0
        and then individually weighing those.
        :return: The heuristic value.
        """
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
        """
        Calculates a heuristic value using 6 base heuristics and converting them to a number between 0.0 and 1.0
        and then scaling those to certain values based on how far the game is from the start to the DYNAMIC_TURN_MAX.

        Currently, the dynamic heuristic has this behaviour:
            Turn 0:
                Score weight loses half value
                Manhattan weight gains the other half of the score weight
            Turn MAX:
                Score weight gains double value (becomes original value)
                Manhattan weight loses all value
                Manhattan opponent weight gains the lost portion of manhattan value

        Update:
            Changed manhattan to scale to 10% of its full value and opponent manhattan to take 90% of its value,
            this is because sometimes manhattan is all we have to go on if no marbles are nearby.

        This ideally will make the agent mainly focus on getting to the center before the opponent does
        at the start of the game. As the game progresses it becomes more aggressive focusing on pushing the
        opponent marbles to the outside and off the board.

        :return: The heuristic value.
        """
        score, score_opponent, \
        manhattan_score, manhattan_opponent_score, \
        adjacency_score, adjacency_opponent_score = cls._composite_normalized(board, player)

        turn_count = 0
        if cls._get_turn_count:
            turn_count = cls._get_turn_count()
        else:
            Debug.log("Warning: Dynamic turn count not setup", DebugType.Warning)

        weight_initial_score = cls.WEIGHT_SCORE / 2
        weight_final_score = cls.WEIGHT_SCORE

        weight_initial_normalized_manhattan = cls.WEIGHT_NORMALIZED_MANHATTAN + weight_initial_score
        weight_final_normalized_manhattan = cls.WEIGHT_NORMALIZED_MANHATTAN * 0.10

        weight_initial_normalized_opponent_manhattan = cls.WEIGHT_NORMALIZED_OPPONENT_MANHATTAN
        weight_final_normalized_opponent_manhattan = cls.WEIGHT_NORMALIZED_OPPONENT_MANHATTAN \
                                                     + (cls.WEIGHT_NORMALIZED_MANHATTAN * 0.90)

        weight_normalized_score = remap(turn_count, 0, cls.DYNAMIC_TURN_MAX,
                                        weight_initial_score,
                                        weight_final_score)

        weight_normalized_manhattan = remap(turn_count, 0, cls.DYNAMIC_TURN_MAX,
                                            weight_initial_normalized_manhattan,
                                            weight_final_normalized_manhattan)

        weight_normalized_opponent_manhattan = remap(turn_count, 0, cls.DYNAMIC_TURN_MAX,
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
        """
        Calculates heuristic value for player score.
        :return: The heuristic value.
        """
        score = board.get_score(player)
        if score >= WIN_SCORE:
            return inf
        return score

    @classmethod
    def _score_opponent(cls, board: Board, player: Color) -> int:
        """
        Calculates heuristic value for opponent score.
        Equals WIN_SCORE when opponent has not pushed any marbles off and -inf
        when they have pushed enough marbles off to win.
        :return: The heuristic value.
        """
        score = board.get_score(Color.next(player))
        if score >= WIN_SCORE:
            return -inf
        return WIN_SCORE - score

    @classmethod
    def _score_optimized(cls, board: Board, player: Color, player_count: int, opponent_count: int) -> int:
        """
        Calculates heuristic value for both scores at the same time.
        :return: The heuristic value.
        """
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
        """
        Calculates heuristic value for centralization of marbles on the board.
        :return: The heuristic value.
        """
        score = 0
        for cell, color in board.enumerate():
            if color is player:
                score += cls.MAX_MANHATTAN_DISTANCE - cell.manhattan(cls.BOARD_CENTER)
        return score

    @classmethod
    def _manhattan_opponent(cls, board: Board, player: Color) -> int:
        """
        Calculates heuristic value for centralization of opponent marbles on the board.
        :return: The heuristic value.
        """
        score = 0
        for cell, color in board.enumerate():
            if color is Color.next(player):
                score += cell.manhattan(cls.BOARD_CENTER)
        return score

    @classmethod
    def _adjacency(cls, board: Board, player: Color) -> int:
        """
        Calculates heuristic value for adjacency of marbles on the board.
        :return: The heuristic value.
        """
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
        """
        Calculates heuristic value for adjacency of opponent marbles on the board.
        :return: The heuristic value.
        """
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
        """
        Normalizes a given score heuristic value between `0.0` and `1.0` except `inf`.
        :return: The normalized heuristic value.
        """
        floor = 0
        ceiling = WIN_SCORE
        if score >= inf:
            return inf
        return remap_01(score, floor, ceiling)

    @classmethod
    def _score_opponent_normalized(cls, score: int) -> float:
        """
        Normalizes a given opponent score heuristic value between `0.0` and `1.0` except `-inf`.
        :return: The normalized heuristic value.
        """
        floor = 0
        ceiling = WIN_SCORE
        if score <= -inf:
            return -inf
        return remap_01(score, floor, ceiling)

    @classmethod
    def _manhattan_normalized(cls, score: int, marble_count: int) -> float:
        """
        Normalizes a given manhattan heuristic value between `0.0` and `1.0`.
        :return: The normalized heuristic value.
        """

        floor = 0
        ceiling_min = 26
        ceiling_max = 36

        ceiling = cls._map_limit_by_marble_count(marble_count, ceiling_min, ceiling_max)
        return clamp_01(remap_01(score, floor, ceiling))

    @classmethod
    def _manhattan_opponent_normalized(cls, score: int, marble_count: int) -> float:
        """
        Normalizes a given opponent manhattan heuristic value between `0.0` and `1.0`.
        :return: The normalized heuristic value.
        """
        floor_min = 10
        floor_max = 20
        ceiling_min = 36
        ceiling_max = 56

        floor = cls._map_limit_by_marble_count(marble_count, floor_min, floor_max)
        ceiling = cls._map_limit_by_marble_count(marble_count, ceiling_min, ceiling_max)

        return clamp_01(remap_01(score, floor, ceiling))

    @classmethod
    def _adjacency_normalized(cls, score: int, marble_count: int) -> float:
        """
        Normalizes a given adjacency heuristic value between `0.0` and `1.0`.
        :return: The normalized heuristic value.
        """
        floor = 0
        ceiling_min = 32
        ceiling_max = 56

        ceiling = cls._map_limit_by_marble_count(marble_count, ceiling_min, ceiling_max)

        return clamp_01(remap_01(score, floor, ceiling))

    @classmethod
    def _adjacency_opponent_normalized(cls, score: int, marble_count: int) -> float:
        """
        Normalizes a given opponent adjacency heuristic value between `0.0` and `1.0`.
        :return: The normalized heuristic value.
        """
        floor_min = 22
        floor_max = 28
        ceiling_min = 54
        ceiling_max = 84

        floor = cls._map_limit_by_marble_count(marble_count, floor_min, floor_max)
        ceiling = cls._map_limit_by_marble_count(marble_count, ceiling_min, ceiling_max)

        return clamp_01(remap_01(score, floor, ceiling))

    @classmethod
    def _composite(cls, board: Board, player: Color) -> tuple[int, int, int, int, int, int, int, int]:
        """
        Calculates all of the 6 base heuristics:
        (Score, Opponent Score, Manhattan, Opponent Manhattan, Adjacency, Opponent Adjacency)

        Calculates these in the most optimal way, enumerating the board once to calculate all heuristics and enumerating
        the board layout once to calculate score heuristics.

        :return: The marbles counts for both players and heuristic values in a tuple of the format:
                 player_count, opponent_count,
                 score, opponent_score,
                 manhattan_score, manhattan_opponent_score,
                 adjacency_score, adjacency_opponent_score
        """
        manhattan_score = 0
        manhattan_opponent_score = 0
        adjacency_score = 0
        adjacency_opponent_score = 0

        player_count = 0
        opponent_count = 0
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
                player_count += 1
                manhattan_score += cls.MAX_MANHATTAN_DISTANCE - cell.manhattan(cls.BOARD_CENTER)
            elif color is Color.next(player):
                opponent_count += 1
                manhattan_opponent_score += cell.manhattan(cls.BOARD_CENTER)
            else:
                pass

        score, opponent_score = cls._score_optimized(board, player, player_count, opponent_count)

        return score, opponent_score, \
               manhattan_score, manhattan_opponent_score, \
               adjacency_score, adjacency_opponent_score, \
               player_count, opponent_count, \

    @classmethod
    def _composite_normalized(cls, board: Board, player: Color) -> tuple[float, float, float, float, float]:
        """
        Uses composite function to calculate the base heuristics and applies normalization functions on the results.

        :return: The normalized heuristic values in a tuple of the format:
                 score, opponent_score,
                 manhattan_score, manhattan_opponent_score,
                 adjacency_score, adjacency_opponent_score
        """

        score, score_opponent, \
        manhattan_score, manhattan_opponent_score, \
        adjacency_score, adjacency_opponent_score, \
        player_count, opponent_count = cls._composite(board, player)

        return cls._score_normalized(score), \
               cls._score_opponent_normalized(score_opponent), \
               cls._manhattan_normalized(manhattan_score, player_count), \
               cls._manhattan_opponent_normalized(manhattan_opponent_score, opponent_count), \
               cls._adjacency_normalized(adjacency_score, player_count), \
               cls._adjacency_opponent_normalized(adjacency_opponent_score, opponent_count)

    @classmethod
    def _map_limit_by_marble_count(cls, count: int, min: Number, max: Number) -> Number:
        """
        Remaps a marble count between min and max based on where it was between MIN_MARBLE_COUNT and MAX_MARBLE_COUNT.
        :return: The remapped value.
        """
        return remap(count, cls.MIN_MARBLE_COUNT, cls.MAX_MARBLE_COUNT, min, max)
