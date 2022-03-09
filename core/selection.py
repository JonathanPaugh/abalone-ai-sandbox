from __future__ import annotations
from typing import TYPE_CHECKING, List

if TYPE_CHECKING:
    from core.board import Board

from lib.hex.hex import Hex, HexDirection


class Selection:
    MAX_SIZE = 3

    def __init__(self, start: Hex, end: Hex = None):
        self.start = start
        self.end = None
        if start != end:
            self.end = end

    def get_player(self, board: Board) -> int:
        """
        :return: Player that owns the cells of selection.
        """
        return board[self.start]

    def get_size(self) -> int:
        """
        :return: The size of the selection.
        """
        if not self.end:
            return 1

        return int(self.start.manhattan(self.end) + 1)

    def get_direction(self) -> HexDirection:
        """
        :return: The direction of the selection from start to end.
        :pre_condition: Selection has size greater than 1.
        """
        if not self.end:
            return None

        size = self.get_size() - 1
        for direction in HexDirection:
            origin = self.start
            for i in range(size):
                origin = origin.add(direction.value)
            if origin == self.end:
                return direction

        return None

    def to_array(self) -> List[Hex]:
        """
        :return: List of the cells in selection.
        """
        cells = [self.start]

        if not self.end:
            return cells

        direction = self.get_direction()
        for i in range(0, self.get_size() - 1):
            next_cell = cells[len(cells) - 1].add(direction.value)
            cells.append(next_cell)

        return cells

    def __str__(self):
        string = str(self.start)
        if self.end:
            string += F", {self.end}"
        return string

    def __eq__(self, other: Selection):
        """
        Determines if `self` and `other` are equivalent.
        :param other: a Selection
        :return: a bool
        """
        if not other:
            return False

        return {self.start, self.end} == {other.start, other.end}

    @classmethod
    def from_array(cls, array: List[Hex]) -> Selection:
        """
        :return: A selection from an array of hexes.
        """
        cls(array[0], array[len(array) - 1])
