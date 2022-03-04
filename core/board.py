from lib.hex_grid import HexGrid
from core.hex import Hex
from constants import BOARD_SIZE

class Board(HexGrid):

    def __init__(self, layout):
        super().__init__(size=BOARD_SIZE)
        self._layout = layout

    @property
    def layout(self):
        return self._layout

    def __str__(self):
        # TODO: return a list of comma-separated "pieces", e.g. A1w
        return super().__str__()

    def __setitem__(self, cell, value):
        super().__setitem__(cell, value)
        if cell in self:
            # mark enumeration struct as in need of recalculation
            # TODO(B): only change the value for the associated item
            self._items = None

    def enumerate(self):
        if not self._items:
            self._items = []
            for r, line in enumerate(self._data):
                for q, val in enumerate(line):
                    q += self.offset(r)
                    item = (Hex(q, r), val)
                    self._items.append(item)
        return self._items
