"""
Defines the game representation.
"""
from agent.heuristics.heuristic import Heuristic
from core.board_layout import BoardLayout
from core.color import Color


class Game:
    """
    The Game class. Analogous to the state representation in our problem
    formulation.
    """

    def __init__(self, starting_layout: BoardLayout = BoardLayout.GERMAN_DAISY):
        self._board = BoardLayout.setup_board(starting_layout)
        self._turn = Color.BLACK

        self.temporary_move_count = [ 0, 0 ]  # Will be removed when history is implemented

    @property
    def board(self):
        """
        Gets the game board.
        :return: a Board
        """
        return self._board

    @property
    def turn(self):
        """
        Gets the color indicating whose turn it is.
        :return: a Color
        """
        return self._turn

    def apply_move(self, move):
        """
        Applies the given move to the game board.
        :param move: the Move to apply
        :return: True if successful, else False
        """

        if self._turn != move.get_player(self._board):
            return False

        self._board.apply_move(move)
        self._next_turn()

        return True

    def _next_turn(self):
        if self._turn == Color.BLACK:
            self.temporary_move_count[0] = 1
        else:
            self.temporary_move_count[1] += 1

        self._turn = Color.next(self._turn)
