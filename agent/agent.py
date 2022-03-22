import random

from agent.state_generator import StateGenerator
from core.board import Board
from core.color import Color
from core.constants import BOARD_SIZE
from core.hex import Hex
from copy import deepcopy
from core.move import Move


class Agent:
    next_move = None

    def find_next_move(self, board: Board, player: Color) -> Move:
        moves = StateGenerator.enumerate_board(board, player)
        # boards = StateGenerator.generate(board, moves)
        # return random.choice(moves)

        best_move = sorted(moves, key=lambda move: self._best_scores(move, player, board=deepcopy(board)))[0]
        return best_move

    def _best_scores(self, move, player, board):
        board.apply_move(move)

        final_score = self._manhattan(board, player)

        return final_score

    def _manhattan(self, board, player):
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


    # def _manhattan(self, boards, player):
    #     # E5 is center of board
    #     center_cell = Hex(4, 5)
    #
    #     # Used to store a list of all the (Hex, Turn) values for the marbles on a current board.
    #     hex_positions = []
    #
    #     # Used to store all the cumulative manhattan distances.
    #     distance_list = []
    #
    #     for board in boards:
    #         hex_positions.append(board.enumerate())
    #
    #     for position in hex_positions:
    #         final_score = 0
    #
    #         for cell in position:
    #             if cell[1] == player:
    #                 final_score += cell[0].manhattan(center_cell)
    #         distance_list.append(final_score)
    #     return distance_list


        # for b in boards:
        #     # Using enumerate function here to get a list of all marble positions in their Hex values +
        #     # player colour it belongs to in the tuple.
        #     list_of_marble_positions_for_board = b.enumerate()
        #
        #     for i in range(0, len(list_of_marble_positions_for_board)):
        #         if list_of_marble_positions_for_board[i][1] == Color.WHITE.value:
        #             distance_corresponding_to_move[i] = list_of_marble_positions_for_board[i][0].manhattan(center_cell)
        #         else:
        #             distance_corresponding_to_move[i] = 1000
        #
        # lowest_distance = 100
        # move_index = None
        # for i in range(0, len(distance_corresponding_to_move)):
        #     if distance_corresponding_to_move[i] < lowest_distance:
        #         lowest_distance = distance_corresponding_to_move[i]
        #         move_index = i
        #
        # return moves[move_index]



