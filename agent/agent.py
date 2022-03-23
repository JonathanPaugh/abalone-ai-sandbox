
from core.constants import BOARD_SIZE
from copy import deepcopy

from agent.state_generator import StateGenerator
from core.board import Board
from core.color import Color
from core.hex import Hex
from core.move import Move

# Initial values of Alpha and Beta
MAX, MIN = 1000, -1000

class Agent:

    def __init__(self):
        # Using class variables to store data from recursion.
        self.best_move = None
        self.node_ordered_yet = False
        self.moves = None

    def find_next_move(self, board: Board, player: Color) -> Move:
        self.moves = StateGenerator.enumerate_board(board, player)
        self.minimax(0, 0, True, board, MIN, MAX, player)
        return self.moves[self.best_move]

    def order_nodes(self, boards, player):
        # Node ordering, sorts nodes based on heuristic value.
        board_heuristics = []
        for i in range(0, len(boards)):
            board_heuristics.append(manhattan_value(boards[i], player))  # HEURISTICS GOES HERE
        for j in range(0, len(boards)):
            for k in range(0, len(boards) - j - 1):
                if board_heuristics[k] < board_heuristics[k + 1]:
                    board_heuristics[k], board_heuristics[k + 1] = board_heuristics[k + 1], board_heuristics[k]
                    boards[k], boards[k + 1] = boards[k + 1], boards[k]
                    self.moves[k], self.moves[k + 1] = self.moves[k + 1], self.moves[k]
        return boards

    def minimax(self, depth, first_layer_index, is_max, board, alpha, beta, player):
        # Minimax with alpha-beta pruning
        # depth is reached
        if depth == 2:
            return manhattan_value(board, player)  # HEURISTIC GOES HERE
        if is_max:
            # MAX
            best_value = MIN
            moves = StateGenerator.enumerate_board(board, player)
            # Node orders if this is the first layer of boards.
            if not self.node_ordered_yet:
                self.node_ordered_yet = True
                deeper_boards = self.order_nodes(StateGenerator.generate(board, moves), player)
            else:
                deeper_boards = StateGenerator.generate(board, moves)

            # for all children of the board
            for i in range(0, len(deeper_boards)):
                if depth == 0:
                    first_layer_index = i
                current_value = self.minimax(depth + 1, first_layer_index, False, deeper_boards[i], alpha, beta, player)
                if current_value > best_value:
                    best_value = current_value
                    # stores best move so far inside class variable.
                    self.best_move = first_layer_index
                alpha = max(alpha, best_value)
                # pruning
                if beta <= alpha:
                    break
            return best_value
        else:
            # MIN
            best_value = MAX
            moves = StateGenerator.enumerate_board(board, opposite_player(player))
            deeper_boards = StateGenerator.generate(board, moves)
            # for all children of the board
            for i in range(0, len(deeper_boards)):
                current_value = self.minimax(depth + 1, first_layer_index, True, deeper_boards[i], alpha, beta, player)
                best_value = min(best_value, current_value)
                beta = min(beta, best_value)
                # pruning
                if beta <= alpha:
                    break
            return best_value



def opposite_player(player):
    # Gets opposite player

    if player == Color.WHITE:
        return Color.BLACK
    return Color.WHITE


def manhattan_value(board, player):
    # Heuristic function using both player's manhattan values

    player_manhattan_score = 0
    opponent_manhattan_score = 0
    center_hex = Hex(4, 4)
    opponent = opposite_player(player)
    positions = board.enumerate()

    for position in positions:
        if position[1] == player:
            player_manhattan_score += 10 - position[0].manhattan(center_hex)
        if position[1] == opponent:
            opponent_manhattan_score += 10 - position[0].manhattan(center_hex)
    return player_manhattan_score - opponent_manhattan_score


#Angela Heuristics and code below here.

# class Agent:
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



