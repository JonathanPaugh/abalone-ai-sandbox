from file_handler import FileHandler
from state_parser import StateParser
import state_generator
from core.board import Board

class Tester:
    def run_tests(self):
        input_amount = None
        while input_amount != 0:
            user_input = input("How many Test.input files are there? Hint: enter 0 to exit: ")

            try:
                input_amount = int(user_input)
                for i in range(0, input_amount):
                    filepath = "Test" + str(i + 1) + ".input"
                    print(filepath)
                    self.test_file(filepath, i + 1)
                break
            except FileNotFoundError:
                print("Number entered does not correspond to number of available Test.input files. "
                      "Only available files processed.")
            except ValueError:
                print("Please enter a number for the number of Test.input files.")

    def test_file(self, filepath, number):
        text = FileHandler.read_file(filepath)

        state, player = StateParser.convert_text_to_state(text)

        board = Board.create_from_data(state)

        generator = state_generator.StateGenerator()

        possible_moves = generator.enumerate_board(board, player)
        possible_boards = generator.generate(board, possible_moves)

        self.write_move_file(possible_moves, number)
        self.write_board_file(possible_boards, number)

    def write_move_file(self, possible_moves, number):
        text = ""
        for move in possible_moves:
            text += F"{str(move)}\n"

        FileHandler.write_file(F"Test{str(number)}.move", text)

    def write_board_file(self, possible_boards, number):
        text = ""
        for board in possible_boards:
            text += F"{StateParser.convert_board_to_text(board)}\n"

        FileHandler.write_file(F"Test{str(number)}.board", text)

    def compare_files(self, input_filepath, compare_filepath):
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
    app = Tester()
    app.run_tests()
    app.compare_files("Test1.board", "Test1.ref")
    app.compare_files("Test2.board", "Test2.ref")
