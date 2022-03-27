"""
Contains definitions for game players.
"""

from enum import Enum


class Color(Enum):
    """
    Indicates a game color, for e.g. turns and piece colors.
    """
    BLACK = 1
    WHITE = 2

    @staticmethod
    def next(color):
        """
        Determines the opposing color from the given color.
        :param color: a Color
        :return: a Color
        """

        if color == Color.BLACK:
            return Color.WHITE

        if color == Color.WHITE:
            return Color.BLACK

    def __str__(self):
        string = super(Color, self).__str__()

        if self == Color.BLACK:
            string += " (BLUE)"

        if self == Color.WHITE:
            string += " (RED)"

        return string
