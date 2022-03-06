"""
Generic logic for a hexagon-shaped grid.
"""

def generate_empty_board(size):
    """
    Generates an empty board with side length `size`.
    :param size: an int
    :precondition size: must be non-negative
    :return: an array of variable-length arrays, each corresponding to a cell in the hex grid
    """
    board = []
    for i in reversed(range(size)):
        board.insert(0, [None] * (size + i))
        if i < size - 1:
            board.append([None] * (size + i))
    return board

class HexGrid:
    """
    A hexagon-shaped grid. Uses offset coordinates where each position is an
    object with `x` and `y` attributes.
    Implements container protocols for the use of `board[cell] = value` and
    `board in cell` syntax.
    """

    def __init__(self, size):
        """
        Initializes a hexagon-shaped grid of the given size.
        :param size: the length of a side of the grid in cells
        """
        self._data = generate_empty_board(size)

    def offset(self, r):
        """
        Determines the grid's x-offset at the given `row`.
        :param r: the row to calculate the x-offset of
        :return: an int
        """
        return (self.height // 2 - r) * (r <= self.height // 2)

    def width(self, r):
        """
        Determines the width of the grid at the given row.
        :param r: the row to calculate the width of the grid at
        :return: an int
        """
        return (len(self._data[r])
            if r >= 0 and r < len(self._data)
            else None)

    def to_array(self):
        data = []
        for row in self._data:
            data_row = []
            for color in row:
                if color:
                    data_row.append(color.value)
                else:
                    data_row.append(0)
            data.append(data_row)

        return data

    @property
    def height(self):
        """
        Determines the height of the grid.
        :return: an int
        """
        return len(self._data)

    def __contains__(self, cell):
        """
        Determines if the grid contains the given `cell`.
        :param cell: an object with `x` and `y` coordinates
        :return: a bool
        """
        q, r = cell.x, cell.y
        q -= self.offset(r)
        return (r >= 0 and r < self.height
            and q >= 0 and q < self.width(r))

    def __getitem__(self, cell):
        """
        Gets the value stored in the grid at the given `cell`.
        Raises IndexError if out of bounds.
        :param cell: an object with `x` and `y` coordinates
        :return: the value stored at the given cell
        """
        if cell not in self:
            raise IndexError(f"grid assignment cell '{cell}' out of range")

        q, r = cell.x, cell.y
        q -= self.offset(r)
        return self._data[r][q]

    def __setitem__(self, cell, value):
        """
        Stores the given `value` in the grid at the given `cell`.
        Raises IndexError if out of bounds.
        :param cell: an object with `x` and `y` coordinates
        :param value: the value to store
        :return: None
        """
        if cell not in self:
            raise IndexError(f"grid cell '{cell}' out of range")

        q, r = cell.x, cell.y
        q -= self.offset(r)
        self._data[r][q] = value
