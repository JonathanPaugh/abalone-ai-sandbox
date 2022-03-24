import math
import time

from core.constants import BOARD_SIZE
from copy import deepcopy

from agent.state_generator import StateGenerator
from core.board import Board
from core.color import Color
from core.hex import Hex
from core.move import Move

from ui.model import Config

# Initial values of Alpha and Beta
MAX, MIN = math.inf, -math.inf
# Center of board used for manhattan value
CENTER_OF_BOARD = Hex(4, 4)
# Sets the time limit given config settings
TIME_LIMIT = Config.DEFAULT_TIME_LIMIT_P1 - 0.5
# Sets the depth limit
DEPTH_LIMIT = 2


class TimeException(Exception):
    # This exception is used to break recursion when given time is up
    pass


class Agent:

    def __init__(self):

        # Stores index of the best move
        self.best_move = None

        # Stores whether the node has been ordered yet
        self.node_ordered_yet = False

        # Stores the ordered moves
        self.moves = None

    def find_next_move(self, board: Board, player: Color) -> Move:
        """
        Finds the next move using minimax with alpha-beta pruning.
        """
        self.node_ordered_yet = False
        self.moves = StateGenerator.enumerate_board(board, player)
        try:
            self.minimax(DEPTH_LIMIT, True, board, MIN, MAX, player, time.time())
        except TimeException:
            print("Times up. Returning.")
            pass
        print("Chosen move: " + str(self.moves[self.best_move]))
        print("Chosen move index: "+str(self.best_move))
        return self.moves[self.best_move]

    def order_nodes(self, boards, player):
        """
        Orders nodes based on their value
        """
        boards, self.moves = map(list, zip(*sorted(zip(boards, self.moves), reverse=True,
                                                   key=lambda x: manhattan_value(x[0], player))))
        return boards

    def minimax(self, depth, is_max, board, alpha, beta, player, start):
        """
        Minimax algorithm with alpha beta pruning.
        Finds the index of the best move.
        """

        # If the time is up, break recursion.
        if time.time() > start + TIME_LIMIT:
            raise TimeException()

        # depth is reached
        if depth == 0:
            return manhattan_value(board, player)  # HEURISTIC GOES HERE

        moves = StateGenerator.enumerate_board(board, player)
        if not self.node_ordered_yet:
            self.node_ordered_yet = True
            deeper_boards = self.order_nodes(StateGenerator.generate(board, moves), player)
        else:
            deeper_boards = StateGenerator.generate(board, moves)

        if is_max:
            # MAX
            best_value = MIN

            # for all children of the board
            for current_board in range(0, len(deeper_boards)):
                board_value = self.minimax(depth - 1, False, deeper_boards[current_board], alpha, beta, player, start)
                if board_value > best_value:
                    best_value = board_value
                    if depth == DEPTH_LIMIT:
                        self.best_move = current_board
                alpha = max(alpha, best_value)

                # pruning
                if beta <= alpha:
                    break
            return best_value
        else:
            # MIN
            best_value = MAX

            # for all children of the board
            for current_board in range(0, len(deeper_boards)):
                board_value = self.minimax(depth - 1, True, deeper_boards[current_board], alpha, beta, player, start)
                best_value = min(best_value, board_value)
                beta = min(beta, best_value)

                # pruning
                if beta <= alpha:
                    break
            return best_value


def manhattan_value(board, player):
    # Heuristic function using both player's manhattan values

    player_manhattan_score = 0
    opponent_manhattan_score = 0
    center_hex = CENTER_OF_BOARD
    opponent = Color.next(player)

    for cell, color in board.enumerate():
        if color == player:
            player_manhattan_score += 10 - cell.manhattan(center_hex)
        if color == opponent:
            opponent_manhattan_score += 10 - cell.manhattan(center_hex)
    return player_manhattan_score - opponent_manhattan_score

    # Angela Heuristics and code below here.

    # class Agent:
    next_move = None

    # def find_next_move(self, board: Board, player: Color) -> Move:
    #     moves = StateGenerator.enumerate_board(board, player)
    #     # boards = StateGenerator.generate(board, moves)
    #     # return random.choice(moves)
    #
    #     best_move = sorted(moves, key=lambda move: self._best_scores(move, player, board=deepcopy(board)))[0]
    #     return best_move
    #
    # def _best_scores(self, move, player, board):
    #     board.apply_move(move)
    #
    #     final_score = self._manhattan(board, player)
    #
    #     return final_score
    #
    # def _manhattan(self, board, player):
    #     hex_positions = [board.enumerate()]
    #     center_cell = Hex(BOARD_SIZE - 1, BOARD_SIZE - 1)
    #
    #     final_score = 0
    #
    #     for p in hex_positions:
    #         manhattan_distance_for_current_cell = 0
    #
    #         for cell in p:
    #
    #             if cell[1] == player:
    #                 manhattan_distance_for_current_cell += cell[0].manhattan(center_cell)
    #         if manhattan_distance_for_current_cell > final_score:
    #             final_score = manhattan_distance_for_current_cell
    #     return final_score

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
