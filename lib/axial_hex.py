from dataclasses import dataclass

@dataclass(frozen=True)
class AxialHex:
    x: int
    y: int

    def __eq__(self, other):
        return self and other and self.x == other.x and self.y == other.y

    def astuple(self):
        return (self.x, self.y)

    def add(self, other):
        return AxialHex(self.x + other.x, self.y + other.y)

    def subtract(self, other):
        return AxialHex(self.x - other.x, self.y - other.y)

    def invert(self):
        return AxialHex(-self.x, -self.y)

    def manhattan(self, other):
        return (abs(self.x - other.x)
            + abs(self.y - other.y)
            + abs(self.x + self.y - other.x - other.y)) / 2

    def adjacent(self, other):
        return self.manhattan(other) == 1
