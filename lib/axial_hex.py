"""
Generic logic for an axial hex coordinate.
"""

from dataclasses import dataclass

@dataclass(frozen=True)
class AxialHex:
    """
    An axial hex coordinate.
    """

    x: int
    y: int

    def __eq__(self, other):
        """
        Determines if `self` and `other` are equivalent.
        :param other: an AxialHex
        :return: a bool
        """
        return self and other and self.x == other.x and self.y == other.y

    def add(self, other):
        """
        Calculates the sum of `self` and `other` non-destructively.
        :param other: an AxialHex
        :return: an AxialHex
        """
        return type(self)(self.x + other.x, self.y + other.y)

    def subtract(self, other):
        """
        Calculates the difference of `self` and `other` non-destructively.
        :param other: an AxialHex
        :return: an AxialHex
        """
        return type(self)(self.x - other.x, self.y - other.y)

    def invert(self):
        """
        Calculates the inversion of `self`.
        :return: an AxialHex
        """
        return type(self)(-self.x, -self.y)

    def manhattan(self, other):
        """
        Finds the manhattan distance between `self` and `other`.
        :param other: an AxialHex
        :return: an AxialHex
        """
        return (abs(self.x - other.x)
            + abs(self.y - other.y)
            + abs(self.x + self.y - other.x - other.y)) / 2

    def adjacent(self, other):
        """
        Determines if `self` and `other` are adjacent cells.
        :param other: an AxialHex
        :return: a bool
        """
        return self.manhattan(other) == 1
