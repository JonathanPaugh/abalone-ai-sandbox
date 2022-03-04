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
    def convert_text_to_state(text) -> tuple[[], int]:
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

        board = []
        turn = 0

        return board, turn