from core.hex import HexDirection, Hex
from move import Move
from selection import Selection


class StateGenerator:
    def __init__(self, handle_get_board):
        self.handle_get_board = handle_get_board

    # returns moves
    def enumerate_board(self, current_player):
        board = self.handle_get_board()
        selections = []
        for cell, color in board.enumerate():
            if self.contains_player_marble(color, current_player):
                temp = self.get_marble_selections(board, cell, current_player)
                for selection in temp:
                    if selection not in selections:
                        selections.append(selection)

        moves = []

        for selection in selections:
            moves.extend(self.get_valid_moves(selection))

        return moves

    def contains_player_marble(self, color, current_player):
        if color:
            return color.value == current_player
        else:
            return False

    def get_marble_selections(self, board, cell, current_player):
        selections = [
            Selection(cell)
        ]

        for direction in HexDirection:
            second_cell = Hex.add(cell, direction.value)
            second_cell = Hex(second_cell.x, second_cell.y)

            if self.is_cell_in_bounds(board, second_cell) and self.contains_player_marble(board[second_cell], current_player):
                selections.append(Selection(cell, second_cell))

                third_cell = Hex.add(second_cell, direction.value)
                third_cell = Hex(third_cell.x, third_cell.y)

                if self.is_cell_in_bounds(board, third_cell) and self.contains_player_marble(board[third_cell], current_player):
                    selections.append(Selection(cell, third_cell))

        return selections

    def is_cell_in_bounds(self, board, cell):
        try:
            board[cell]
        except IndexError:
            return False

        return True

    def get_valid_moves(self, selection):
        moves = []

        for direction in HexDirection:
            move = Move(selection, direction)
            if self.is_valid_move(move):
                moves.append(move)

        return moves

    def is_valid_move(self, move):
        return True
