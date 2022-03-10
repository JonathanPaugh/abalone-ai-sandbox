from __future__ import absolute_import

from os.path import splitext
from lib.file_handler import FileHandler
from parse import state_parser
from agent import state_generator
from core.board import Board
from glob import glob

import re
import os

class Tester:
    """
    This class contains the methods needed to read input from test files and
    generates files of all possible moves and their resulting board states.
    """
    def run_tests(self):
        """
        Creates output folder, finds and tests each test.input file.
        :return: none
        """
        if not os.path.exists("dist"):
            os.makedirs("dist")

        try:
            for file in glob("Test*.input"):
                path, ext = splitext(file)
                number = re.search("\\d+$", path).group()
                self.test_file(F"{path}{ext}", number)
        except FileNotFoundError:
            print("Test<#>.input file(s) not found.")

    def test_file(self, filepath, number):
        """
        Reads a text file and generates all moves and their resulting board states and writes them to output files.
        :param filepath: a String containing path of file
        :param number: an int representing the current test<#>.input
        :return: none
        """
        text = FileHandler.read_file(filepath)

        state, player = state_parser.StateParser().convert_text_to_state(text)

        board = Board.create_from_data(state)

        generator = state_generator.StateGenerator()

        possible_moves = generator.enumerate_board(board, player)
        possible_boards = generator.generate(board, possible_moves)

        self.write_move_file(possible_moves, number)
        self.write_board_file(possible_boards, number)

    def write_move_file(self, possible_moves, number):
        """
        Writes the list of moves into an output file.
        :param possible_moves: list of possible moves
        :param number: an int representing the current test<#>.input
        :return: none
        """
        text = ""
        for move in possible_moves:
            text += F"{state_parser.StateParser().convert_move_to_text(move)}\n"

        FileHandler.write_file(F"dist/Test{str(number)}.move", text)

    def write_board_file(self, possible_boards, number):
        """
            Writes the list of boards into an output file.
            :param possible_boards: list of possible boards
            :param number: an int representing the current test<#>.input
            :return: none
            """
        text = ""
        for board in possible_boards:
            text += F"{state_parser.StateParser().convert_board_to_text(board)}\n"

        FileHandler.write_file(F"dist/Test{str(number)}.board", text)

    def compare_files(self, input_filepath, compare_filepath):
        """
        Compares 2 files containing lines of possible boards.
        :param input_filepath: a string containing file path name
        :param compare_filepath: a string containing file path name to be compared
        :return: none
        """
        input_data = FileHandler.read_file(input_filepath).splitlines()
        compare_data = FileHandler.read_file(compare_filepath).splitlines()

        print(F"Comparing Files: {input_filepath} => {compare_filepath}")

        for i in range(0, len(input_data)):
            found = False
            for compare_line in compare_data:
                if input_data[i] == compare_line:
                    found = True
                    break

            if not found:
                print(F"Unable to find match for row: {i + 1}")

        print(F"Comparison Complete")


if __name__ == "__main__":
    print("Program Started")
    app = Tester()
    app.run_tests()
    print("Program Completed: Output files generated in 'dist' folder.")
