"""
Contains Abalone-specific hex grid logic.
"""

from lib.hex_grid import HexGrid
from core.hex import Hex
from constants import BOARD_SIZE

class Board(HexGrid):
    """
    A hex grid specific to the game of Abalone.
    Implements serialization, extra iteration helpers, and a reference to
    starting layout data for headlessly calculating game score.
    """

    def __init__(self, layout):
        """
        Initializes a game board.
        :param layout: the starting BoardLayout
        """
        super().__init__(size=BOARD_SIZE)
        self._layout = layout
        self._items = None

    @property
    def layout(self):
        """
        Gets the board's starting layout.
        Used for headlessly calculating game score.
        """
        return self._layout

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
