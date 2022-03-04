def translate_to_board(string):
    pass


def get_board():
    return [[0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0]]


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


class StateParser:
    @staticmethod
    def convert_board_to_text(board) -> str:
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

        C5b,D5b,E4b,E5b,E6b,F5b,F6b,F7b,F8b,G6b,H6b,C3w,C4w,D3w,D4w,D6w,E7w,F4w,G5w,G7w,G8w,G9w,H7w,H8w,H9w

        """

        text = ""

        return text

    @staticmethod
    def convert_text_to_state(filename) -> tuple[[], int]:
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

        board = get_board()
        with open(filename) as file:
            data = file.read().rstrip()
            turn_color = (data[0])
            untranslated_list = data[2:].split(",")
            for string in untranslated_list:
                translated = translate_text_to_board(string)
                board[translated[0]][translated[1] - 1] = translated[2]

            print(board)
        return board, int(turn_color)
