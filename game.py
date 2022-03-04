import game_ui
from board_layout import BoardLayout
from state_generator import StateGenerator


class Game:
    """
    This class represents a game object and contains methods for display and settings.
    """

    TITLE = "Abalone"

    def __init__(self):
        self.board = self.generate_board(BoardLayout.Standard)
        self.game_ui = game_ui.GameUI(lambda: self.board)

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
        self.board = self.generate_board(layout)

    def generate_board(self, layout):
        """
        Sets the game layout based on the given parameter.
        :param layout: an int
        :return: None
        """
        layout_options = {
            BoardLayout.Standard: self.generate_standard_layout,
            BoardLayout.German: self.generate_german_layout,
            BoardLayout.Belgian: self.generate_belgian_layout
        }
        return layout_options[layout]()

    @staticmethod
    def generate_standard_layout():
        """
        Represents a standard layout board.
        :return: board as a 2d array.
        """
        return [
            [1, 1, 1, 1, 1],
            [1, 1, 1, 1, 1, 1],
            [0, 0, 1, 1, 1, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 2, 2, 2, 0, 0],
            [2, 2, 2, 2, 2, 2],
            [2, 2, 2, 2, 2],
        ]

    @staticmethod
    def generate_german_layout():
        """
        Represents a german layout board.
        :return: board as a 2d array.
        """
        return [
            [0, 0, 0, 0, 0],
            [1, 1, 0, 0, 2, 2],
            [1, 1, 1, 0, 2, 2, 2],
            [0, 1, 1, 0, 0, 2, 2, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 2, 2, 0, 0, 1, 1, 0],
            [2, 2, 2, 0, 1, 1, 1],
            [2, 2, 0, 0, 1, 1],
            [0, 0, 0, 0, 0],
        ]

    @staticmethod
    def generate_belgian_layout():
        """
        Represents a belgian layout board.
        :return: board as a 2d array.
        """
        return [
            [1, 1, 0, 2, 2],
            [1, 1, 1, 2, 2, 2],
            [0, 1, 1, 0, 2, 2, 0],
            [0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0],
            [0, 2, 2, 0, 1, 1, 0],
            [2, 2, 2, 1, 1, 1],
            [2, 2, 0, 1, 1],
        ]
