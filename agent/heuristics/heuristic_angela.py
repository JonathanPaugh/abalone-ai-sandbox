from core.constants import BOARD_SIZE
from core.hex import Hex


def manhattan(board, player):
    hex_positions = [board.enumerate()]
    center_cell = Hex(BOARD_SIZE - 1, BOARD_SIZE - 1)

    final_score = 0

    for p in hex_positions:
        manhattan_distance_for_current_cell = 0

        for cell in p:

            if cell[1] == player:
                manhattan_distance_for_current_cell += cell[0].manhattan(center_cell)
        if manhattan_distance_for_current_cell > final_score:
            final_score = manhattan_distance_for_current_cell

    return final_score
