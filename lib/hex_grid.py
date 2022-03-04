def generate_empty_board(size):
  board = []
  for i in reversed(range(size)):
    board.insert(0, [None] * (size + i))
    if i < size - 1:
      board.append([None] * (size + i))
  return board

class HexGrid:

    def __init__(self, size):
        self._data = generate_empty_board(size)

    def offset(self, r):
        return (self.height // 2 - r) * (r <= self.height // 2)

    def width(self, r):
        return (len(self._data[r])
            if r >= 0 and r < len(self._data)
            else None)

    @property
    def height(self):
        return len(self._data)

    def __contains__(self, cell):
        q, r = cell.x, cell.y
        q -= self.offset(r)
        return (r >= 0 and r < self.height
            and q >= 0 and q < self.width(r))

    def __getitem__(self, cell):
        if cell not in self:
            return None
        q, r = cell.x, cell.y
        q -= self.offset(r)
        return self._data[r][q]

    def __setitem__(self, cell, value):
        if cell in self:
            q, r = cell.x, cell.y
            q -= self.offset(r)
            self._data[r][q] = value
