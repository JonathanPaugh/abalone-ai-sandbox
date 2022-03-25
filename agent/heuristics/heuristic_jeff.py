from agent.heuristics.heuristic import Heuristic
from core.color import Color


def manhattan(board, player):
    player_manhattan_score = 0
    opponent_manhattan_score = 0

    opponent = Color.next(player)

    for cell, color in board.enumerate():
        if color == player:
            player_manhattan_score += Heuristic.MAX_MANHATTAN_DISTANCE - cell.manhattan(Heuristic.BOARD_CENTER)
        if color == opponent:
            opponent_manhattan_score += Heuristic.MAX_MANHATTAN_DISTANCE - cell.manhattan(Heuristic.BOARD_CENTER)

    return player_manhattan_score - opponent_manhattan_score
