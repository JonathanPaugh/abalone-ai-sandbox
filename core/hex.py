from enum import Enum
from lib.axial_hex import AxialHex
from lib.lerp import lerp
from constants import BOARD_MAXCOLS

# neighbor cache to avoid neighborhood recalculation
HEX_NEIGHBORS = {}

class Hex(AxialHex):

    def __repr__(self):
        return f"{chr(BOARD_MAXCOLS - self.y + ord('A') - 1)}{self.x + 1}"

    def lerp(self, other, time):
        return Hex(
            x=lerp(self.x, other.x, time),
            y=lerp(self.y, other.y, time),
        )

    def neighbors(self):
        self_tuple = (self.x, self.y)
        if self_tuple not in HEX_NEIGHBORS:
            HEX_NEIGHBORS[self_tuple] = [self.add(d.value) for d in HexDirection]
        return HEX_NEIGHBORS[self_tuple]

class HexDirection(Enum):
    NW = Hex(0, -1)
    NE = Hex(1, -1)
    W = Hex(-1, 0)
    E = Hex(1, 0)
    SW = Hex(-1, 1)
    SE = Hex(0, 1)

    @staticmethod
    def resolve(direction):
        return next((d for d in HexDirection if d.value == direction), None)
