from core.board_layout import BoardLayout
from core.color import Color


class Game:
    """
    This class represents a game object and contains methods for display and settings.
    """

    def __init__(self, board_layout=BoardLayout.STANDARD):
        self._board = BoardLayout.setup_board(board_layout)
        self._turn = Color.BLACK

    @property
    def board(self):
        return self._board

    @property
    def turn(self):
        return self._turn

    def apply_move(self, move):
        if self._turn != move.selection.get_player(self._board): # TODO: demeter
            return False

        self._board.apply_move(move)
        self._turn = Color.next(self._turn)
        return True
