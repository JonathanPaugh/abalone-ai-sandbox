import math

from agent.heuristics.heuristic import Heuristic
from agent.state_generator import StateGenerator
from core.board import Board
from core.color import Color
from core.constants import MAX_SELECTION_SIZE

# Initial values of Alpha and Beta
MAX, MIN = math.inf, -math.inf
# Sets the depth limit
DEPTH_LIMIT = 2


class TimeException(Exception):
    # This exception is used to break recursion when given time is up
    pass


class Search:
    def __init__(self):
        # Stores index of the best move
        self.best_move = 0

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
        self.best_move = 0
        self.node_ordered_yet = False
        self.interrupt = False
        self.moves = StateGenerator.enumerate_board(board, player)

        try:
            self.minimax(DEPTH_LIMIT, True, board, MIN, MAX, player, on_find_move)
        except TimeException:
            pass

        print("Chosen Move: " + str(self.moves[self.best_move]))
        print("Chosen Move Index: " + str(self.best_move))

    def minimax(self, depth, is_max, board, alpha, beta, player, on_find_move):
        """
        Minimax algorithm with alpha beta pruning.
        Finds the index of the best move.
        """

        # If the time is up, break recursion.
        if self.interrupt:
            raise TimeException()

        # depth is reached
        if depth == 0:
            return Heuristic.main(board, player)

        moves = StateGenerator.enumerate_board(board, player if is_max else Color.next(player))

        if not self.node_ordered_yet:
            self.node_ordered_yet = True
            deeper_boards = self.order_nodes(StateGenerator.generate(board, moves))
        else:
            deeper_boards = StateGenerator.generate(board, moves)

        if is_max:
            # MAX
            best_value = MIN

            # for all children of the board
            for current_board in range(0, len(deeper_boards)):
                board_value = self.minimax(depth - 1, False, deeper_boards[current_board], alpha, beta, player, on_find_move)
                if board_value > best_value:
                    best_value = board_value
                    if depth == DEPTH_LIMIT:
                        self.best_move = current_board
                        on_find_move(self.moves[current_board])
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
                board_value = self.minimax(depth - 1, True, deeper_boards[current_board], alpha, beta, player, on_find_move)
                best_value = min(best_value, board_value)
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
