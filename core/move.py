from __future__ import annotations
from typing import TYPE_CHECKING, List
from core.hex import Hex, HexDirection
from core.selection import Selection
from core.constants import BOARD_MAX_COLS

if TYPE_CHECKING:
    from core.board import Board, Color


class Move:

    @staticmethod
    def decode_cell(cell_str: str) -> Hex:
        """
        Decodes a cell string to a hex coordinate e.g. E5 -> Hex(4, 4)
        :param cell_str: a str
        :return: a Hex
        """
        CODEPOINT_A = 65
        col = int(cell_str[1]) - 1
        row = BOARD_MAX_COLS - ord(cell_str[0]) + CODEPOINT_A - 1
        return Hex(col, row)

    @classmethod
    def decode(cls, move_str):
        """
        Decodes a move string
        :param move_str: a str
        :return: a Move
        """
        direction, start, end = move_str[1:-1].split(", ")
        return Move(
            selection=Selection(cls.decode_cell(start), cls.decode_cell(end)),
            direction=HexDirection[direction],
        )

    def __init__(self, selection: Selection, direction: HexDirection):
        self.selection = selection
        self.direction = direction

    def __str__(self):
        return f"({self.direction.name}, {self.selection})"

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

    def get_back(self) -> Hex:
        """
        :return: Cell in back of selection relative to move direction.
        :precondition: Move is inline.
        """
        if not self.is_inline():
            return None

        test_cell = self.selection.start.add(self.direction.value)

        if test_cell in self.selection.to_array():
            return self.selection.start

        return self.selection.end

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

    def get_front_target(self) -> Hex:
        if not self.is_inline():
            return None

        return self.get_front().add(self.direction.value)

    def get_destinations(self) -> List[Hex]:
        """
        :return: List of destination cells for each origin cell from selection.
        """
        destinations = []
        for cell in self.selection.to_array():
            destinations.append(cell.add(self.direction.value))

        return destinations

    def get_player(self, board: Board) -> Color:
        """
        :return: Player that owns the cells of the move selection.
        """
        return self.selection.get_player(board)

    def get_cells(self) -> List[Hex]:
        """
        :return: List of the cells in the move selection.
        """
        return self.selection.to_array()
