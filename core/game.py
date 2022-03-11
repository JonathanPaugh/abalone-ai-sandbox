from core.board_layout import BoardLayout


class Game:
    """
    This class represents a game object and contains methods for display and settings.
    """

    def __init__(self, board_layout=BoardLayout.STANDARD):
        self.board = BoardLayout.setup_board(board_layout)
