"""
Contains logic for board layout management.
"""

from json import loads
from enum import Enum
from core.board import Board

def _load_board_data_from_file_path(file_path):
    """
    Loads a JSON file from the given file path.
    :param file_path: The file path to load the JSON from.
    :precondition file_path: a JSON file at `file_path` must exist relative to driver root
    :return: a JSON object (str, list, or dict)
    """
    with open(file_path, mode="r", encoding="utf-8") as file:
        return loads(file.read())

class BoardLayout(Enum):
    """
    A collection of standard board layouts.
    The value side of a board layout is an array of variable-length arrays
    in the shape of an offset hex grid.
    """

    STANDARD = _load_board_data_from_file_path("layouts/standard.json")
    GERMAN_DAISY = _load_board_data_from_file_path("layouts/german_daisy.json")
    BELGIAN_DAISY = _load_board_data_from_file_path("layouts/belgian_daisy.json")

    def setup_board(board_layout):
        """
        Generates a board from the given board layout.
        :param board_layout: a BoardLayout
        :return: a Board
        """
        return Board.create_from_data(data=board_layout.value)
