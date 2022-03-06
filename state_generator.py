from typing import List

from core.board import Board
from core.color import Color
from core.hex import HexDirection, Hex
import game
from move import Move
from selection import Selection
from state_parser import StateParser, translate_board_to_text


class StateGenerator:
    def __init__(self, handle_get_board):
        self.handle_get_board = handle_get_board

    def test_generator(self, current_player: int):
        moves = self.enumerate_board(current_player)
        boards = self.generate_state_space(moves)
        for i in range(len(moves)):
            print(F"{i + 1} => {moves[i]}")

        counter = 0
        for board in boards:
            print(F"{counter + 1} => {translate_board_to_text(board)}")
            counter += 1

    def generate_state_space(self, moves: List[Move]) -> List[Board]:
        states = []
        for move in moves:
            states.append(self.generate_next_board(move))

        return states

    def generate_next_board(self, move: Move) -> Board:
        """
        Need to add summito logic.
        """
        board = Board.create_from_data(self.handle_get_board().to_array())

        return self._apply_base_move(board, move)


    def _apply_sumito_move(self, board: Board, move: Move) -> Board:
        return self._apply_base_move(board, move)

    def _apply_base_move(self, board: Board, move: Move) -> Board:
        player = move.selection.get_player(board)

        for cell in move.selection.to_array():
            board[cell] = None

        for cell in move.get_destinations():
            board[cell] = player

        return board

    def enumerate_board(self, current_player: int) -> List[Move]:
        board = self.handle_get_board()
        selections = []
        for cell, color in board.enumerate():
            if self.contains_player_marble(color, current_player):
                temp = self.get_possible_selections(board, cell, current_player)
                for selection in temp:
                    if selection not in selections:
                        selections.append(selection)

        moves = []
        for selection in selections:
            moves.extend(self.get_valid_moves(board, selection, current_player))

        return moves

    def contains_player_marble(self, color: int, current_player: int) -> bool:
        if color:
            return color.value == current_player
        return False

    def get_possible_selections(self, board: Board, cell: Hex, current_player: int) -> List[Selection]:
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

    def is_cell_in_bounds(self, board: Board, cell: Hex) -> bool:
        try:
            board[cell]
        except IndexError:
            return False

        return True

    def get_valid_moves(self, board: Board, selection: Selection, current_player: int) -> List[Move]:
        moves = []

        for direction in HexDirection:
            move = Move(selection, direction)
            if self.is_valid_move(board, move, current_player):
                moves.append(move)

        return moves

    def is_valid_move(self, board: Board, move: Move, current_player: int) -> bool:
        if move.is_single():
            return self.is_valid_single_move(board, move)

        if move.is_inline():
            return self.is_valid_inline_move(board, move, current_player)

        return self.is_valid_sidestep_move(board, move)

    def is_valid_single_move(self, board: Board, move: Move) -> bool:
        destination = move.selection.start.add(move.direction.value)

        if not self.is_cell_in_bounds(board, destination):
            return False

        if board[destination]:
            return False

        return True


    def is_valid_inline_move(self, board: Board, move: Move, current_player: int) -> bool:
        """
        I think out of bounds logic doesnt make sense for sumitos that push off a marble,
        they would not be valid but they should be. Need to fix.
        """
        distance = 0
        destination = move.get_front()

        while distance < game.Game.MAX_SUMITO:
            distance += 1
            destination = destination.add(move.direction.value)
            if not self.is_cell_in_bounds(board, destination):
                return False
            if not board[destination]:
                return True
            if board[destination] == Color(current_player):
                return False
            else:
                if distance >= move.selection.get_size():
                    return False

        return True

    def is_valid_sidestep_move(self, board: Board, move: Move) -> bool:
        for cell in move.selection.to_array():
            destination = cell.add(move.direction.value)

            if not self.is_cell_in_bounds(board, destination):
                return False

            if board[destination]:
                return False

        return True
