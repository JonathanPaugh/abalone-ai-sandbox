from math import inf
from numbers import Number

from core.board import Board
from core.color import Color
from core.constants import BOARD_SIZE, WIN_SCORE, HEX_CONSTANT
from core.hex import Hex


class Heuristic:
    MAX_MANHATTAN_DISTANCE = BOARD_SIZE - 1
    BOARD_CENTER = Hex(BOARD_SIZE - 1, BOARD_SIZE - 1)

    @classmethod
    def main(cls, board: Board, player: Color) -> Number:
        return cls.weighted(board, player)

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
    def score_opponent(cls, board: Board, player: Color) -> int:
        score = board.get_score(Color.next(player))
        if score >= WIN_SCORE:
            return -inf
        return WIN_SCORE - score

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
    def manhattan_normalized(cls, board: Board, player: Color) -> float:
        count = board.get_marble_count(player)
        adjustment = cls._get_manhattan_normalized_adjustment(count)
        manhattan_average = (cls.manhattan(board, player) + adjustment) / count  # Get average between 0 and 4
        return manhattan_average / cls.MAX_MANHATTAN_DISTANCE  # Scale to 0.0 to 1.0

    @classmethod
    def manhattan_opponent_normalized(cls, board: Board, player: Color) -> float:
        return 1.0 - cls.manhattan_normalized(board, Color.next(player))

    @classmethod
    def _get_manhattan_normalized_adjustment(cls, count: int):
        """
        Calculate manhattan normalized adjustment.

        Ex:
        If we have 2 marbles the best we can do is the center cell and any cell next to it
        This means we would lose a value of 1 due to a marble being offset one cell from the center,
        so we set the adjustment to 1 and added to the manhattan value.

        If we have 8 marbles the best we can do is the center cell and the next ring around the center cell for
        all the marbles plus any cell next to that ring. This means we would lose a value of 8
        (6 for each marble in the adjacent ring and 2 for the single marble outside that ring)
        The adjustment is set to 8 and added to the manhattan value.
        """

        adjustment = 0
        depth = 0
        depth_ceiling = 1
        count_remaining = count - 1
        while depth_ceiling < count:
            cells_in_depth = (depth * HEX_CONSTANT)
            depth_ceiling += cells_in_depth

            while count_remaining > 0 and cells_in_depth > 0:
                adjustment += depth
                count_remaining -= 1
                cells_in_depth -= 1

            depth += 1

        return adjustment
