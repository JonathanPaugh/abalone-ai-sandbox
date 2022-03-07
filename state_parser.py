"""This module contains methods to read parse input/output files containing current board states."""
from typing import Tuple

from core.board import Board
from core.color import Color


class StateParser:
    """
    This class contains the functions and methods to parse Test.input files into a usable notation for our program
    and vice versa.
    """
    empty_board_layout = \
        [
            [0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0]
        ]

    # Keep for testing translate_board_to_text.
    test_output_board_layout = \
        [
            [0, 0, 0, 0, 0],
            [2, 2, 0, 0, 1, 1],
            [2, 2, 2, 0, 1, 1, 1],
            [0, 2, 2, 0, 0, 1, 1, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 1, 1, 0, 0, 2, 2, 0],
            [1, 1, 1, 0, 2, 2, 2],
            [1, 1, 0, 0, 2, 2],
            [0, 0, 0, 0, 0]
        ]

    @classmethod
    def convert_text_to_state(cls, text) -> Tuple[Board, int]:
        """
        Converts Test.input state representation into our own representation.
        :param text: a string containing Test.input state representation.
        :return: a tuple containing our state representation
        """
        board = cls.empty_board_layout
        data = text.rstrip()
        turn_color = (data[0])
        if turn_color == 'b':
            turn_color = 1
        else:
            turn_color = 2
        untranslated_list = data[2:].split(",")
        for string in untranslated_list:
            translated = cls._translate_text_to_board(string)
            board[translated[0]][translated[1] - 1] = translated[2]

        return board, int(turn_color)

    @classmethod
    def convert_board_to_text(cls, board: Board):
        """
        Given a board representation, return a string containing all the occupied cells.
        :param board: a board in our state representation
        :return: a string containing the state representation in the test.board notation
        """

        temp_positions = ""

        current_state = Board.enumerate(board)
        for marbles, colour in current_state:
            if colour is not None:
                if colour == Color.BLACK:
                    player = "b"
                else:
                    player = "w"
                temp_positions += str(marbles) + player + ", "
        positions_list = temp_positions.split(" ")
        positions_list.sort()
        string_positions = "".join(map(str, positions_list))

        return cls._sort_text(string_positions[:(len(string_positions) - 1)])

    @staticmethod
    def _translate_text_to_board(string):
        """
        Translates a single piece from Test.input into our own piece notation.
        :param string: a string containing information from Test.input
        :return:
        """
        mapping = {
            "A": 8,
            "B": 7,
            "C": 6,
            "D": 5,
            "E": 4,
            "F": 3,
            "G": 2,
            "H": 1,
            "I": 0,
        }

        if ord(string[0]) > ord('E'):
            position = int(string[1]) - int(ord(string[0]) - ord('E'))
        else:
            position = int(string[1])
        if string[2] == "b":
            colour = 1
        else:
            colour = 2
        return [mapping[string[0]], position, colour]

    @staticmethod
    def _sort_text(string):
        """
        Sorts the pieces based on the colour, Y-axis and X-axis.
        :param string: a string of unsorted pieces
        :return: a string of sorted pieces
        """
        list_text = string.split(",")
        value = {
            "b": 1000,
            "w": 100,
            "A": 90,
            "B": 80,
            "C": 70,
            "D": 60,
            "E": 50,
            "F": 40,
            "G": 30,
            "H": 20,
            "I": 10,
        }
        sorted_dict = {}
        positions = []
        for text in list_text:
            position = int(value[text[0]]) + 10-int(text[1]) + int(value[text[2]])
            positions.append(position)
            sorted_dict[position] = text
        positions.sort(reverse=True)
        concat = ""
        for pos in positions:
            concat += sorted_dict[pos] + ","
        return concat[:-1]
