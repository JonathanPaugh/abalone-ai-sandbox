"""This module contains methods to read parse input/output files containing current board states."""

from core.board import Board
from core.color import Color


class StateParser:
    # Possibly to keep track of the Test<#>.board later? As per instructions.
    # output_board_num = 1
    #
    # @classmethod
    # def increase_text_output_num(cls):
    #     cls.output_board_num += 1

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
    def convert_text_to_state(cls, filename) -> tuple[[], int]:
        """
        Convert the text in format (including turn) b=player 1, w=player 2:
        b
        C5b,D5b,E4b,E5b,E6b,F5b,F6b,F7b,F8b,G6b,H6b,C3w,C4w,D3w,D4w,D6w,E7w,F4w,G5w,G7w,G8w,G9w,H7w,H8w,H9w
        to a state:
        ([
             [0, 0, 0, 0, 0],
             [2, 2, 0, 0, 1, 1],
             [2, 2, 2, 0, 1, 1, 1],
             [0, 2, 2, 0, 0, 1, 1, 0],
             [0, 0, 0, 0, 0, 0, 0, 0, 0],
             [0, 1, 1, 0, 0, 2, 2, 0],
             [1, 1, 1, 0, 2, 2, 2],
             [1, 1, 0, 0, 2, 2],
             [0, 0, 0, 0, 0],
        ], 1)
        """

        board = cls.empty_board_layout
        with open(filename) as file:
            data = file.read().rstrip()
            turn_color = (data[0])
            if turn_color == 'b':
                turn_color = 2
            else:
                turn_color = 1
            untranslated_list = data[2:].split(",")
            for string in untranslated_list:
                translated = translate_text_to_board(string)
                board[translated[0]][translated[1] - 1] = translated[2]

            print(board)
        return board, int(turn_color)

    @staticmethod
    def convert_board_to_text(filename, board: Board):
        """
        convert the board ex:
        [
             [0, 0, 0, 0, 0],
             [2, 2, 0, 0, 1, 1],
             [2, 2, 2, 0, 1, 1, 1],
             [0, 2, 2, 0, 0, 1, 1, 0],
             [0, 0, 0, 0, 0, 0, 0, 0, 0],
             [0, 1, 1, 0, 0, 2, 2, 0],
             [1, 1, 1, 0, 2, 2, 2],
             [1, 1, 0, 0, 2, 2],
             [0, 0, 0, 0, 0],
        ]
        to the text format (not including turn):
        C5b,D5b,E4b,E5b,E6b,F5b,F6b,F7b,F8b,G6b,H6b,C3w,C4w,D3w,D4w,D6w,E7w,F4w,G5w,G7w,G8w,G9w,H7w,H8w,H9w and
        writes to a Test<#>.board plaintext file.
        """

        with open(filename, mode="w") as f:
            f.write(translate_board_to_text(board))

    @staticmethod
    def convert_move_to_text(self, move) -> str:
        """
        Convert the move object to a move notation:
        EX:
        NW, C3, C4
        """

        text = ""
        return text


def translate_text_to_board(string):
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
        colour = 2
    else:
        colour = 1
    return [mapping[string[0]], position, colour]


def translate_board_to_text(board: Board) -> str:
    """Given a board representation, return a string containing all the occupied cells."""
    tempt_positions = ""

    current_state = Board.enumerate(board)
    for marbles, colour in current_state:
        if colour is not None:
            if colour == Color.BLACK:
                player = "b"
            else:
                player = "w"
            tempt_positions += str(marbles) + player + ", "
    positions_list = tempt_positions.split(" ")
    positions_list.sort()
    string_positions = "".join(map(str, positions_list))
    #For testing.
    print(string_positions[:(len(string_positions) - 1)])
    return string_positions[:(len(string_positions) - 1)]


if __name__ == "__main__":
    parser = StateParser
    board_layout = Board().create_from_data(parser.test_output_board_layout)
    parser.convert_board_to_text("Test1.board", board_layout)

    parser.convert_text_to_state("Test1.input")
