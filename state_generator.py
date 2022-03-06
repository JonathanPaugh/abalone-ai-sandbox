from __future__ import annotations
from typing import List

from core.board import Board
from core.hex import HexDirection, Hex
from move import Move
from selection import Selection
from state_parser import StateParser

class StateGenerator:
    def test_generator(self, board, current_player: int):
        moves = self.enumerate_board(board, current_player)
        boards = self.generate(board, moves)
        for i in range(len(moves)):
            print(F"{i + 1} => {moves[i]}")
        for i in range(len(boards)):
            print(F"{i + 1} => {StateParser.convert_board_to_text(board)}")

    def generate(self, board: Board, moves: List[Move]) -> List[Board]:
        boards = []
        for move in moves:
            next_board = Board.create_from_data(board.to_array())
            next_board.apply_move(move)
            boards.append(next_board)

        return boards

    def enumerate_board(self, board, current_player: int) -> List[Move]:
        selections = []
        for cell, _ in board.enumerate():
            if board.cell_owned_by(cell, current_player):
                temp = self._get_possible_selections(board, cell, current_player)
                for selection in temp:
                    if selection not in selections:
                        selections.append(selection)

        moves = []
        for selection in selections:
            moves.extend(self._get_valid_moves(board, selection, current_player))

        return moves

    def _get_possible_selections(self, board: Board, cell: Hex, current_player: int) -> List[Selection]:
        selections = [
            Selection(cell)
        ]

        for direction in HexDirection:
            next_cell = cell

            for i in range(Selection.MAX_SIZE - 1):
                next_cell = Hex.add(next_cell, direction.value)
                next_cell = Hex(next_cell.x, next_cell.y)

                if board.cell_in_bounds(next_cell) and board.cell_owned_by(next_cell, current_player):
                    selections.append(Selection(cell, next_cell))
                else:
                    break

        return selections

    def _get_valid_moves(self, board: Board, selection: Selection, current_player: int) -> List[Move]:
        moves = []

        for direction in HexDirection:
            move = Move(selection, direction)
            if board.is_valid_move(move, current_player):
                moves.append(move)

        return moves
