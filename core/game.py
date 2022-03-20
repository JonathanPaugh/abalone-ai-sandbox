"""
Defines the game representation.
"""

from core.board_layout import BoardLayout
from core.color import Color
from ui.model.config import Config


class Game:
    """
    The Game class. Analogous to the state representation in our problem
    formulation.
    """

    def __init__(self, config=Config.from_default()):
        self._config = config
        self._board = BoardLayout.setup_board(config.layout)
        self._turn = Color.BLACK

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

    @property
    def config(self):
        """
        Gets the game config.
        :return: a Config
        """
        return self._config

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
        self._turn = Color.next(self._turn)