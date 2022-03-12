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
        if color == Color.BLACK:
            return Color.WHITE

        if color == Color.WHITE:
            return Color.BLACK
