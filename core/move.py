from __future__ import annotations
from typing import TYPE_CHECKING, List

if TYPE_CHECKING:
    from core.board import Board
    from core.hex import Hex, HexDirection
    from selection import Selection


class Move:
    def __init__(self, selection: Selection, direction: HexDirection):
        self.selection = selection
        self.direction = direction

    def is_single(self) -> bool:
        """
        :return: If the selection is a single cell.
        """
        return self.selection.get_size() <= 1

    def is_inline(self) -> bool:
        """
        :return: If the move is parallel to the selection.
        """
        if self.is_single():
            return False

        return self.selection.get_direction().is_parallel(self.direction)

    def is_sumito(self, board: Board) -> bool:
        """
        :return: If the move is inline the destination is an occupied cell.
        :precondition: Move is validated. (Does not check destination owner)
        """
        if not self.is_inline():
            return False

        destination = self.get_front().add(self.direction.value)

        if board[destination]:
            return True

        return False

    def get_front(self) -> Hex:
        """
        :return: Cell in front of selection relative to move direction.
        :precondition: Move is inline.
        """
        if not self.is_inline():
            return None

        test_cell = self.selection.start.add(self.direction.value)

        if test_cell not in self.selection.to_array():
            return self.selection.start

        return self.selection.end

    def get_destinations(self) -> List[Hex]:
        """
        :return: List of destination cells for each origin cell from selection.
        """
        destinations = []
        for cell in self.selection.to_array():
            destinations.append(cell.add(self.direction.value))

        return destinations

    def __str__(self):
        string = F"({self.direction.name}, {self.selection})"
        return string
