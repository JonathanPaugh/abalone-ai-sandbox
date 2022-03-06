import game_ui
import state_generator
from core.board_layout import BoardLayout

class Game:
    """
    This class represents a game object and contains methods for display and settings.
    """

    TITLE = "Abalone"

    def __init__(self):
        self.board = BoardLayout.setup_board(BoardLayout.TEST)
        self.game_ui = game_ui.GameUI()
        self.state_generator = state_generator.StateGenerator()
        self.state_generator.test_generator(self.board, 1)

    def get_board(self):
        return self.board

    def display(self, parent, **kwargs):
        """
        This method displays the GUI though a function call.
        :param parent: the GUI base
        :param kwargs: dictionary of arguments
        :return:
        """
        self.game_ui.display(parent, self.board, **kwargs)

    def update_settings(self, config):
        """
        Sets up a new layout from the given config settings.
        :param config: a config.
        :return:
        """
        self.board = BoardLayout.setup_board(config.layout)
