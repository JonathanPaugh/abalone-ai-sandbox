class StateGenerator:
    def enumerate_board(self, board, player):
        for row in board:
            for tile in row:
                print(tile, end="")
            print()
