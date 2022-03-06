from typing import List

from core.board import Board
from core.hex import Hex, HexDirection
from selection import Selection


class Move:
    def __init__(self, selection: Selection, direction: HexDirection):
        self.selection = selection
        self.direction = direction

    def __str__(self):
        string = F"({self.direction}, {self.selection})"
        return string

    def is_single(self) -> bool:
        return self.selection.get_size() <= 1

    def is_inline(self) -> bool:
        if self.is_single():
            return False

        return self.selection.get_direction().same_axis(self.direction)

    def is_sumito(self, board: Board) -> bool:
        if self.is_inline():
            return False

        destination = self.get_front().add(self.direction.value)

        if board[destination]:
            return True

        return False

    def get_front(self) -> Hex:
        if not self.is_inline():
            return None

        test_cell = self.selection.start.add(self.direction.value)

        if test_cell not in self.selection.to_array():
            return self.selection.start

        return self.selection.end

    def get_destinations(self) -> List[Hex]:
        destinations = []
        for cell in self.selection.to_array():
            destinations.append(cell.add(self.direction.value))

        return destinations
