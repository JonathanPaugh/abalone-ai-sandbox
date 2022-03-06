import state_parser
from state_generator import StateGenerator
from state_parser import StateParser
from core.board import Board


def write_move_file(possible_moves, number):
    file_move = open("Test" + str(number) + ".move", "w")
    for moves in possible_moves:
        file_move.write(moves.__str__())
        file_move.write("\n")
    file_move.close()


def write_board_file(possible_boards, number):
    file_board = open("Test" + str(number) + ".board", "w")
    for board in possible_boards:
        file_board.write(state_parser.translate_board_to_text(board))
        file_board.write("\n")
    file_board.close()


class Tester:
    def run_tests(self):
        input_amount = None

        while input_amount != 0:
            user_input = input("How many Test.input files are there? Hint: enter 0 to exit: ")

            try:
                input_amount = int(user_input)
                for i in range(0, input_amount):
                    file = "Test" + str(i+1) + ".input"
                    print(file)
                    self.test_file(file, i+1)
            except FileNotFoundError:
                print("Number entered does not correspond to number of available Test.input files. Only available files"
                      " processed.")
            except ValueError:
                print("Please enter a number for the number of Test.input files.")

    def test_file(self, file, number):

        initial_state = StateParser.convert_text_to_state(file)
        print(initial_state)

        the_board = Board.create_from_data(initial_state[0])

        generator = StateGenerator(the_board)

        possible_moves = generator.enumerate_board(initial_state[1])

        possible_boards = []
        for move in possible_moves:
            possible_boards.append(generator.generate_next_board(move))

        write_move_file(possible_moves, number)
        write_board_file(possible_boards, number)


if __name__ == "__main__":
    app = Tester()
    app.run_tests()
