"""
Contains Abalone-specific hex grid logic.
"""

from __future__ import annotations

from selection import Selection
from move import Move
from core.color import Color
from core.hex import Hex
from constants import BOARD_SIZE
from lib.hex_grid import HexGrid


class Board(HexGrid):
    """
    A hex grid specific to the game of Abalone.
    Implements serialization, extra iteration helpers, and a reference to
    starting layout data for headlessly calculating game score.
    """

    MAX_SUMITO = 3

    @staticmethod
    def create_from_data(data):
        """
        Creates a board from the given board data.
        The original board data is cached within the board for score calculations.
        :param data: an array of arrays of domain 0..2
        :return: a Board
        """
        board = Board()
        board._layout = data
        for r, line in enumerate(data):
            for q, val in enumerate(line):
                q += board.offset(r) # offset coords - board storage starts at x with size - 1
                cell = Hex(q, r)
                try:
                    board[cell] = Color(val)
                except ValueError:
                    board[cell] = None
        return board

    def __init__(self):
        """
        Initializes a game board.
        """
        super().__init__(size=BOARD_SIZE)
        self._layout = None
        self._items = None

    @property
    def layout(self):
        """
        Gets the board's starting layout.
        Used for headlessly calculating game score.
        """
        return self._layout

    def enumerate(self):
        """
        Returns all positions and values on the game board a la `enumerate`.
        :return: a list of (Hex, T) tuples
        """
        if not self._items:
            self._items = []
            for r, line in enumerate(self._data):
                for q, val in enumerate(line):
                    q += self.offset(r)
                    item = (Hex(q, r), val)
                    self._items.append(item)
        return self._items

    def cell_in_bounds(self, cell: Hex) -> bool:
        try:
            self[cell]
        except IndexError:
            return False

        return True

    def cell_owned_by(self, cell: Hex, player: int) -> bool:
        return self[cell] and self[cell].value == player

    def is_valid_move(self, move: Move, current_player: int) -> bool:
        if move.is_single():
            return self._is_valid_single_move(move)

        if move.is_inline():
            return self._is_valid_inline_move(move, current_player)

        return self._is_valid_sidestep_move(move)

    def apply_move(self, move: Move):
        self._apply_sumito_move(move) if move.is_sumito(self) else self._apply_base_move(move)

    def _is_valid_single_move(self, move: Move) -> bool:
        destination = move.selection.start.add(move.direction.value)

        if not self.cell_in_bounds(destination):
            return False

        if self[destination]:
            return False

        return True

    def _is_valid_inline_move(self, move: Move, current_player: int) -> bool:
        destination = move.get_front()
        out_of_bounds_valid = False
        for i in range(1, self.MAX_SUMITO + 1):
            destination = destination.add(move.direction.value)
            if not self.cell_in_bounds(destination):
                return out_of_bounds_valid
            if not self[destination]:
                return True
            if self[destination] == Color(current_player):
                return False
            else:
                if i >= move.selection.get_size():
                    return False

                out_of_bounds_valid = True

        return True

    def _is_valid_sidestep_move(self, move: Move) -> bool:
        for cell in move.selection.to_array():
            destination = cell.add(move.direction.value)

            if not self.cell_in_bounds(destination):
                return False

            if self[destination]:
                return False

        return True

    def _apply_base_move(self, move: Move):
        player = move.selection.get_player(self)

        for cell in move.selection.to_array():
            self[cell] = None

        for cell in move.get_destinations():
            self[cell] = player

    def _apply_sumito_move(self, move: Move):
        destination = move.get_front().add(move.direction.value)

        start = Hex(destination.x, destination.y)
        while self.cell_in_bounds(destination.add(move.direction.value)) and self[destination.add(move.direction.value)]:
            destination = destination.add(move.direction.value)

        sumito_move = Move(Selection(start, Hex(destination.x, destination.y)), move.direction)

        player = sumito_move.selection.get_player(self)

        for cell in sumito_move.selection.to_array():
            if not self.cell_in_bounds(cell):
                print(sumito_move.selection)
            else:
                self[cell] = None

        for cell in sumito_move.get_destinations():
            if self.cell_in_bounds(cell):
                self[cell] = player

        self._apply_base_move(move)

    def __str__(self):
        # TODO: return a list of comma-separated "pieces", e.g. A1w
        return super().__str__()

    def __setitem__(self, cell, value):
        """
        Sets the value on the board at position `cell` to `value`.
        :param cell: a Hex
        :param value: the value to set
        """
        super().__setitem__(cell, value)
        if cell in self:
            # mark enumeration struct as in need of recalculation
            # TODO(B): only change the value for the associated item
            self._items = None