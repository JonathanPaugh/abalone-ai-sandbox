from state_generator import StateGenerator
from state_parser import StateParser


class Tester:
    def run_tests(self):
        files = []

        for file in files:
            self.test_file(file)

    def test_file(self, file):
        text = ""  # Get text from file

        initial_state = StateParser.convert_text_to_state(text)

        generator = StateGenerator()

        possible_states = generator.enumerate_board(initial_state[0], initial_state[1])

        representations = map(lambda state: StateParser.convert_board_to_text(state[0]), possible_states)

        # Create and open output file
        output_file = None

        for representation in representations:
            # Append representations to output file
            pass


if __name__ == "__main__":
    app = Tester()
    app.run_tests()
