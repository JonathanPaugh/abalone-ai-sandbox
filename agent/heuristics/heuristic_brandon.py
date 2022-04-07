from dataclasses import dataclass
from core.hex import Hex
from core.constants import BOARD_SIZE


@dataclass(frozen=True)
class HeuristicWeights:
    """
    Models heuristic weights.
    """
    score: int
    score_opponent: int
    centralization: int
    centralization_opponent: int
    adjacency: int
    adjacency_opponent: int


def heuristic_offensive(board, color):
    """
    An offensive heuristic.
    """
    return heuristic(board, color, HeuristicWeights(
        score=15,
        score_opponent=30,
        centralization=1,
        centralization_opponent=1.25,
        adjacency=0.1,
        adjacency_opponent=0.15
    ))

def heuristic_defensive(board, color):
    """
    A defensive heuristic.
    """
    return heuristic(board, color, HeuristicWeights(
        score=15,
        score_opponent=25,
        centralization=1,
        centralization_opponent=1,
        adjacency=0.1,
        adjacency_opponent=0.125
    ))


def heuristic(board, color, weights):
    MAX_MARBLES = 14
    BOARD_RADIUS = BOARD_SIZE - 1
    BOARD_CENTER = Hex(BOARD_RADIUS, BOARD_RADIUS)

    heuristic_score = MAX_MARBLES
    heuristic_score_opponent = MAX_MARBLES
    heuristic_centralization = 0
    heuristic_centralization_opponent = 0
    heuristic_adjacency = 0
    heuristic_adjacency_opponent = 0

    for cell, cell_color in board.enumerate_nonempty():
        cell_centralization = BOARD_RADIUS - Hex.manhattan(cell, BOARD_CENTER)
        cell_adjacency = sum([
            board[n] == cell_color if n in board else 0
                for n in Hex.neighbors(cell)
        ])
        cell_adjacency = pow(cell_adjacency / 2, 2)

        if cell_color == color:
            heuristic_centralization += cell_centralization
            heuristic_adjacency += cell_adjacency
            heuristic_score_opponent -= 1
        else:
            heuristic_centralization_opponent += cell_centralization
            heuristic_adjacency_opponent += cell_adjacency
            heuristic_score -= 1

    return (
        weights.score * heuristic_score
        - weights.score_opponent * heuristic_score_opponent
        + weights.centralization * heuristic_centralization
        - weights.centralization_opponent * heuristic_centralization_opponent
        + weights.adjacency * heuristic_adjacency
        - weights.adjacency_opponent * heuristic_adjacency_opponent
    )
