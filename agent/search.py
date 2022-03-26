import math

from agent.heuristics.heuristic import Heuristic
from agent.state_generator import StateGenerator
from core.board import Board
from core.color import Color
from core.constants import MAX_SELECTION_SIZE

# Initial values of Alpha and Beta
from core.move import Move

MAX, MIN = math.inf, -math.inf
# Sets the depth limit
DEPTH_LIMIT = 4


class TimeException(Exception):
    # This exception is used to break recursion when given time is up
    pass


class Search:
    def __init__(self):
        # Stores index of the best move
        self.best_heuristic = 0

        # Stores whether the node has been ordered yet
        self.node_ordered_yet = False

        # Stores the ordered moves
        self.moves = None

        # Flags when exception should be called based on in-game timer.
        self.interrupt = False

    def find_next_move(self, board: Board, player: Color, on_find_move: callable):
        """
        Finds the next move using minimax with alpha-beta pruning.
        """
        self.best_heuristic = 0
        self.node_ordered_yet = False
        self.interrupt = False

        try:
            self.minimax_j_max(board, player, None, MIN, MAX, DEPTH_LIMIT, DEPTH_LIMIT, on_find_move)
            # self.minimax(0, 0, True, board, MIN, MAX, player, on_find_move)
        except TimeException:
            pass


    # Try best move separate from alpha #
    def minimax_j_max(self, board: Board, player: Color, original_move: Move,
                      alpha: int, beta: int, depth, depth_limit: int, on_find_move: callable):
        if self.interrupt:
            raise TimeException()

        if depth <= 0:
            return original_move, Heuristic.main(board, player)

        best_node = None, MIN

        moves = StateGenerator.enumerate_board(board, player)
        boards = StateGenerator.generate(board, moves)
        transitions = list(zip(moves, boards))

        for move, next_board in transitions:
            if depth >= depth_limit:
                original_move = move

            node_move, node_heuristic = self.minimax_j_min(next_board, player, original_move,
                                      alpha, beta, depth - 1, depth_limit, on_find_move)

            best_node = max(best_node, (node_move, node_heuristic), key=lambda n: n[1])

            if depth >= depth_limit:
                if best_node[1] > self.best_heuristic:
                    self.best_heuristic = best_node[1]
                    print(F"Original: {original_move}, Move: {best_node[0]}, Heuristic {best_node[1]}")
                    on_find_move(best_node[0])

            if best_node[1] > beta:
                return best_node

            alpha = max(alpha, best_node[1])

        return best_node

    def minimax_j_min(self, board: Board, player: Color, original_move: Move,
                      alpha: int, beta: int, depth: int, depth_limit: int, on_find_move: callable):
        if self.interrupt:
            raise TimeException()

        if depth <= 0:
            return original_move, Heuristic.main(board, player)

        best_node = None, MAX

        moves = StateGenerator.enumerate_board(board, Color.next(player))
        boards = StateGenerator.generate(board, moves)

        for next_board in boards:
            node = self.minimax_j_max(next_board, player, original_move,
                                      alpha, beta, depth - 1, depth_limit, on_find_move)
            best_node = min(best_node, node, key=lambda n: n[1])

            if best_node[1] < alpha:
                return best_node

            beta = min(beta, best_node[1])

        return best_node

    def minimax(self, depth, first_layer_index, is_max, board, alpha, beta, player, on_find_move):
        # Minimax with alpha-beta pruning
        # depth is reached
        if depth > DEPTH_LIMIT:
            return Heuristic.main(board, player)  # HEURISTIC GOES HERE
        if is_max:
            # MAX
            best_value = MIN
            moves = StateGenerator.enumerate_board(board, player)
            # Node orders if this is the first layer of boards.
            if not self.node_ordered_yet:
                self.node_ordered_yet = True
                deeper_boards = self.order_nodes(StateGenerator.generate(board, moves))
            else:
                deeper_boards = StateGenerator.generate(board, moves)

            # for all children of the board
            for i in range(0, len(deeper_boards)):
                if depth == 0:
                    first_layer_index = i
                    print(F"{moves[first_layer_index]}, {Heuristic.main(deeper_boards[i], player)}")
                current_value = self.minimax(depth + 1, first_layer_index, False, deeper_boards[i], alpha, beta, player, on_find_move)
                if current_value > best_value:
                    best_value = current_value
                    # stores best move so far inside class variable.
                    self.best_move = first_layer_index
                    on_find_move(self.moves[self.best_move])
                alpha = max(alpha, best_value)
                # pruning
                if beta <= alpha:
                    break
            return best_value
        else:
            # MIN
            best_value = MAX
            moves = StateGenerator.enumerate_board(board, Color.next(player))
            deeper_boards = StateGenerator.generate(board, moves)
            # for all children of the board
            for i in range(0, len(deeper_boards)):
                current_value = self.minimax(depth + 1, first_layer_index, True, deeper_boards[i], alpha, beta, player, on_find_move)
                best_value = min(best_value, current_value)
                beta = min(beta, best_value)
                # pruning
                if beta <= alpha:
                    break
            return best_value

    def order_nodes(self, boards):
        """
        Orders nodes based on their value
        """

        # transitions = list(zip(boards, self.moves))
        # transitions.sort(key=lambda transition: self._order_move(transition[0], transition[1]), reverse=True)
        # boards, self.moves = map(list, zip(*transitions))

        return boards

    def _order_move(self, board,  move):
        if move.is_sumito(board):
            return MAX_SELECTION_SIZE + 1
        return len(move.get_cells())
