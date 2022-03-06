"""
Contains Abalone-specific grid cell logic.
"""

from __future__ import annotations
from enum import Enum
from lib.axial_hex import AxialHex
from lib.lerp import lerp
from constants import BOARD_MAXCOLS

# neighbor cache to avoid neighborhood recalculation
HEX_NEIGHBORS = {}

class Hex(AxialHex):
    """
    A hex cell specific to the game of Abalone.
    """

    def __str__(self):
        """
        Returns the current cell in Abalone move notation, e.g. A1 etc.
        :return: a string
        """
        return f"{chr(BOARD_MAXCOLS - self.y + ord('A') - 1)}{self.x + 1}"

    def lerp(self, other, time):
        """
        Interpolates the cell between `self` and `other` at `time`%.
        Used primarily for animation logic.
        :param other: the ending cell to interpolate to
        :param time: the time to interpolate to
        :return: a Hex
        """
        return Hex(
            x=lerp(self.x, other.x, time),
            y=lerp(self.y, other.y, time),
        )

    def neighbors(self):
        """
        Finds all six neighbors of this cell.
        :return: a list[Hex]
        """
        self_tuple = (self.x, self.y)
        if self_tuple not in HEX_NEIGHBORS: # cache neighbors (ok with 61 cells)
            HEX_NEIGHBORS[self_tuple] = [self.add(d.value) for d in HexDirection]
        return HEX_NEIGHBORS[self_tuple]

class HexDirection(Enum):
    """
    The collection of all six hex directions.
    """

    NW = Hex(0, -1)
    NE = Hex(1, -1)
    W = Hex(-1, 0)
    E = Hex(1, 0)
    SW = Hex(-1, 1)
    SE = Hex(0, 1)

    def is_parallel(self, other: HexDirection) -> bool:
        return abs(self.value.x) == abs(other.value.x) and \
               abs(self.value.y) == abs(other.value.y)

    def get_opposite(self) -> HexDirection:
        return HexDirection(self.value.invert())

    @staticmethod
    def resolve(direction: Hex) -> HexDirection:
        """
        Resolves a direction from a Hex value.
        Use over `HexDirection(direction)` if working with calculated normals.
        :param direction: a Hex
        :return: a HexDirection
        """
        return next((d for d in HexDirection if d.value == direction), None)
