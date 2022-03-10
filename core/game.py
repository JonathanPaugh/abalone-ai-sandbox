from core.board_layout import BoardLayout


class Game:
    """
    This class represents a game object and contains methods for display and settings.
    """

    def __init__(self):
        self.board = BoardLayout.setup_board(BoardLayout.STANDARD)

    def update_settings(self, config):
        """
        Sets up a new layout from the given config settings.
        :param config: a config.
        :return:
        """
        self.board = BoardLayout.setup_board(config.layout)
