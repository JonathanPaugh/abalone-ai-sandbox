from core.board import Board


def translate_to_board(string):
    pass

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


def get_board():
    return [
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
    # return [[0, 0, 0, 0, 0],
    #         [0, 0, 0, 0, 0, 0],
    #         [0, 0, 0, 0, 0, 0, 0],
    #         [0, 0, 0, 0, 0, 0, 0, 0],
    #         [0, 0, 0, 0, 0, 0, 0, 0, 0],
    #         [0, 0, 0, 0, 0, 0, 0, 0],
    #         [0, 0, 0, 0, 0, 0, 0],
    #         [0, 0, 0, 0, 0, 0],
    #         [0, 0, 0, 0, 0]]


def translate_text_to_board(string):
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
    string_positions = ""
    current_state = Board.enumerate(board)
    print(current_state)
    for marbles, colour in current_state:
        if colour is not None:
            if colour == 1:
                player = "b"
            else:
                player = "w"
            string_positions += marbles + player + ", "
    print(string_positions)
    return string_positions


class StateParser:
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

        C5b,D5b,E4b,E5b,E6b,F5b,F6b,F7b,F8b,G6b,H6b,C3w,C4w,D3w,D4w,D6w,E7w,F4w,G5w,G7w,G8w,G9w,H7w,H8w,H9w

        """

        with open(filename, mode="w") as f:
            f.write(translate_board_to_text(board))

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


    def convert_move_to_text(self, move) -> str:
        """
        Convert the move object to a move notation:
        EX:

        NW, C3, C4
        """

        text = ""
        return text


if __name__ == "__main__":
    parser = StateParser
    board = Board(get_board())
    parser.convert_board_to_text("Test1.board", board)



    #
    # test = Board.enumerate(board)
    # print(test)
    # row = 0
    # list_of_tuples = [(Hex(x=4, y=0), None), (Hex(x=5, y=0), None)]
    # for position, colour in list_of_tuples:
    #     x = list_of_tuples[row][0].get_x
    #     y = list_of_tuples[row][0].get_y
    #     if colour == 1:
    #         text_colour = 2
    #     elif colour == 2:
    #         text_colour = 2
    #     else:
    #         text_colour = 0
    #     row += 1
    #     print(x, y, text_colour)
    #
    # print(list_of_tuples[0][0])

