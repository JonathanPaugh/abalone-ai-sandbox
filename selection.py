from __future__ import annotations
from typing import TYPE_CHECKING, List
if TYPE_CHECKING:
    from core.board import Board

from core.hex import Hex, HexDirection

class Selection:
    MAX_SIZE = 3

    def __init__(self, start: Hex, end: Hex=None):
        self.start = start
        self.end = None
        if start != end:
            self.end = end

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

    def get_player(self, board: Board) -> int:
        return board[self.start]

    def get_size(self) -> int:
        if not self.end:
            return 1

        return int(self.start.manhattan(self.end) + 1)

    def get_direction(self) -> HexDirection:
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
        cells = [self.start]

        if not self.end:
            return cells

        direction = self.get_direction()
        for i in range(0, self.get_size() - 1):
            next_cell = cells[len(cells) - 1].add(direction.value)
            cells.append(Hex(next_cell.x, next_cell.y))

        return cells

    @classmethod
    def from_array(cls, array: List[Hex]) -> Selection:
        cls(array[0], array[len(array) - 1])

