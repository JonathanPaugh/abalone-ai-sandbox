from random import getrandbits
from core.board import Board


ZOBRIST_BITS = 64


def _setup_cell_table():
    table = {}
    temp_board = Board()
    for i, (cell, _) in enumerate(temp_board.enumerate()):
        table[cell] = i
    return table

cell_table = _setup_cell_table()


def _setup_zobrist(num_bits):
    table = {}
    for i in range(2):
        piece_index = i + 1
        for _, cell_index in cell_table.items():
            table[cell_index * piece_index] = getrandbits(num_bits)
    return table

zobrist_table = _setup_zobrist(num_bits=ZOBRIST_BITS)
