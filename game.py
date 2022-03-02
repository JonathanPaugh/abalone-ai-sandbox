import game_ui
from board_layout import BoardLayout


class Game:
    """
    This class represents a game object and contains methods for display and settings.
    """

    TITLE = "Abalone"

    def __init__(self):
        self.game_ui = game_ui.GameUI()
        self.window = None

    def display(self, parent, **kwargs):
        """
        This method displays the GUI though a function call.
        :param parent: the GUI base
        :param kwargs: dictionary of arguments
        :return:
        """
        self.game_ui.display(parent, **kwargs)

    def update_settings(self, config):
        """
        Sets up a new layout from the given config settings.
        :param config: a config.
        :return:
        """
        layout = BoardLayout.from_string(config.layout)
        self.game_ui.set_layout(layout)
