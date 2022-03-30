from core.hex import Hex
from core.constants import BOARD_SIZE


WEIGHT_SCORE = 15
WEIGHT_SCORE_OPPONENT = 25
WEIGHT_CENTRALIZATION = 1
WEIGHT_CENTRALIZATION_OPPONENT = 0.5
WEIGHT_ADJACENCY = 0.05
WEIGHT_ADJACENCY_OPPONENT = 0.025


def heuristic(board, color):
    MAX_MARBLES = 14
    BOARD_RADIUS = BOARD_SIZE - 1
    BOARD_CENTER = Hex(BOARD_RADIUS, BOARD_RADIUS)

    heuristic_score = MAX_MARBLES
    heuristic_score_opponent = MAX_MARBLES
    heuristic_centralization = 0
    heuristic_centralization_opponent = 0
    heuristic_adjacency = 0
    heuristic_adjacency_opponent = 0

    for cell, cell_color in board.enumerate():
        if cell_color is None:
            continue

        cell_centralization = BOARD_RADIUS - Hex.manhattan(cell, BOARD_CENTER)
        cell_adjacency = sum([
            board[n] == cell_color if n in board else 0
                for n in Hex.neighbors(cell)
        ])
        cell_adjacency = pow(cell_adjacency, 2)

        if cell_color == color:
            heuristic_centralization += cell_centralization
            heuristic_adjacency += cell_adjacency
            heuristic_score_opponent -= 1
        else:
            heuristic_centralization_opponent += cell_centralization
            heuristic_adjacency_opponent += cell_adjacency
            heuristic_score -= 1

    return (
        WEIGHT_SCORE * heuristic_score
        - WEIGHT_SCORE_OPPONENT * heuristic_score_opponent
        + WEIGHT_CENTRALIZATION * heuristic_centralization
        - WEIGHT_CENTRALIZATION_OPPONENT * heuristic_centralization_opponent
        + WEIGHT_ADJACENCY * heuristic_adjacency
        - WEIGHT_ADJACENCY_OPPONENT * heuristic_adjacency_opponent
    )
