from json import loads
from enum import Enum
from core.board import Board
from core.color import Color
from core.hex import Hex

def load_board_layout_from_file_name(file_name):
    with open(file_name, mode="r") as file:
        file_buffer = file.read()
    return loads(file_buffer)

class BoardLayout(Enum):
    STANDARD = load_board_layout_from_file_name("layouts/standard.json")
    GERMAN_DAISY = load_board_layout_from_file_name("layouts/german_daisy.json")
    BELGIAN_DAISY = load_board_layout_from_file_name("layouts/belgian_daisy.json")

    def setup_board(board_layout):
        board = Board(layout=board_layout)
        for r, line in enumerate(board_layout.value):
            for q, val in enumerate(line):
                q += board.offset(r)
                board[Hex(q, r)] = Color(val)
        return board

    def num_units(board_layout, color):
        num_units = 0
        for line in board_layout.value:
            for val in line:
                num_units += val == color.value
        return num_units
