import math

from agent.heuristics.heuristic import Heuristic
from agent.state_generator import StateGenerator
from core.board import Board
from core.color import Color
from core.constants import MAX_SELECTION_SIZE
from core.move import Move


class Search:
    DEPTH_LIMIT = 3
    MIN = -math.inf
    MAX = math.inf

    def __init__(self):
        self.interrupt = False

    def alpha_beta(self, board: Board, player: Color, on_find_move: callable):
        """
        Finds the next move using minimax with alpha-beta pruning.
        """
        self.interrupt = False

        try:
            self._alpha_beta_max(board, player, None, self.MIN, self.MAX,
                                 self.DEPTH_LIMIT, self.DEPTH_LIMIT, on_find_move)

        except TimeoutException:
            pass

    def _alpha_beta_max(self, board: Board, player: Color, original_move: Move,
                        alpha: int, beta: int, depth, depth_limit: int, on_find_move: callable):
        if self.interrupt:
            raise TimeoutException()

        if depth <= 0:
            return Heuristic.main(board, player)

        best_heuristic = self.MIN

        moves = StateGenerator.enumerate_board(board, player)
        boards = StateGenerator.generate(board, moves)
        transitions = list(zip(moves, boards))

        if depth >= depth_limit:
            self._order_nodes(board, transitions)

        for move, next_board in transitions:
            if depth >= depth_limit:
                original_move = move

            heuristic = self._alpha_beta_min(next_board, player, original_move,
                                             alpha, beta, depth - 1, depth_limit, on_find_move)

            best_heuristic = max(best_heuristic, heuristic)

            if depth >= depth_limit:
                if best_heuristic > alpha:
                    on_find_move(original_move)

            if best_heuristic > beta:
                return best_heuristic

            alpha = max(alpha, best_heuristic)

        return best_heuristic

    def _alpha_beta_min(self, board: Board, player: Color, original_move: Move,
                        alpha: int, beta: int, depth: int, depth_limit: int, on_find_move: callable):
        if self.interrupt:
            raise TimeoutException()

        if depth <= 0:
            return Heuristic.main(board, player)

        best_heuristic = self.MAX

        moves = StateGenerator.enumerate_board(board, Color.next(player))
        boards = StateGenerator.generate(board, moves)

        for next_board in boards:
            heuristic = self._alpha_beta_max(next_board, player, original_move,
                                             alpha, beta, depth - 1, depth_limit, on_find_move)

            best_heuristic = min(best_heuristic, heuristic)

            if best_heuristic < alpha:
                return best_heuristic

            beta = min(beta, best_heuristic)

        return best_heuristic

    @classmethod
    def _order_nodes(cls, board, transitions):
        """
        Orders nodes based on their value
        """
        transitions.sort(key=lambda transition: cls._order_move(transition[0], board), reverse=True)

    @staticmethod
    def _order_move(move, board):
        if move.is_sumito(board):
            return MAX_SELECTION_SIZE + 1
        return len(move.get_cells())

    def _alpha_beta_old(self, depth, first_layer_index, is_max, board, alpha, beta, player, on_find_move):
        # Minimax with alpha-beta pruning
        # depth is reached
        if depth > self.DEPTH_LIMIT:
            return Heuristic.main(board, player)  # HEURISTIC GOES HERE
        if is_max:
            # MAX
            best_value = self.MIN
            moves = StateGenerator.enumerate_board(board, player)
            # Node orders if this is the first layer of boards.
            if not self.node_ordered_yet:
                self.node_ordered_yet = True
                deeper_boards = self._order_nodes(StateGenerator.generate(board, moves))
            else:
                deeper_boards = StateGenerator.generate(board, moves)

            # for all children of the board
            for i in range(0, len(deeper_boards)):
                if depth == 0:
                    first_layer_index = i
                    print(F"{moves[first_layer_index]}, {Heuristic.main(deeper_boards[i], player)}")
                current_value = self._alpha_beta_old(depth + 1, first_layer_index, False, deeper_boards[i], alpha, beta, player, on_find_move)
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
            best_value = self.MAX
            moves = StateGenerator.enumerate_board(board, Color.next(player))
            deeper_boards = StateGenerator.generate(board, moves)
            # for all children of the board
            for i in range(0, len(deeper_boards)):
                current_value = self._alpha_beta_old(depth + 1, first_layer_index, True, deeper_boards[i], alpha, beta, player, on_find_move)
                best_value = min(best_value, current_value)
                beta = min(beta, best_value)
                # pruning
                if beta <= alpha:
                    break
            return best_value


class TimeoutException(Exception):
    pass
