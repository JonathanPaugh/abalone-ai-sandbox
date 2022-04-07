"""
Defines the game representation.
"""
from core.board import Board
from core.board_layout import BoardLayout
from core.color import Color
from ui.debug import DebugType, Debug
from ui.model import config


class Game:
    """
    The Game class. Analogous to the state representation in our problem
    formulation.
    """

    def __init__(self, starting_layout: BoardLayout = BoardLayout.STANDARD):
        self._board = BoardLayout.setup_board(starting_layout)
        self._turn = Color.BLACK

    def set_board(self, board: Board):
        self._board = board

    @property
    def board(self) -> Board:
        """
        Gets the game board.
        :return: a Board
        """
        return self._board

    @property
    def turn(self) -> Color:
        """
        Gets the color indicating whose turn it is.
        :return: a Color
        """
        return self._turn

    def set_turn(self, player: Color):
        """
        Sets the color representing whose turn it is.
        :param player: a Color
        """
        self._turn = player

    def apply_move(self, move) -> bool:
        """
        Applies the given move to the game board.
        :param move: the Move to apply
        :return: True if successful, else False
        """

        if self._turn != move.get_player(self._board):
            Debug.log("Warning: Tried to apply move for the wrong player", DebugType.Warning)
            return False

        self._board.apply_move(move)
        self._next_turn()

        return True

    def _next_turn(self):
        """
        Makes the game to progress to the next turn.
        """
        self._turn = Color.next(self._turn)
