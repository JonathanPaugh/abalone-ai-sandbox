from __future__ import annotations
from typing import List

from core.board import Board
from core.color import Color
from core.hex import HexDirection, Hex
from core.move import Move
from core.selection import Selection
from parse.state_parser import StateParser


class StateGenerator:

    @classmethod
    def test(cls, board: Board, current_player: Color):
        """
        Tests agent generation functions on a board by printing out each resulting move and agent.
        """
        moves = cls.enumerate_board(board, current_player)
        boards = cls.generate(board, moves)
        for i in range(len(moves)):
            print(F"{i + 1} => {StateParser.convert_move_to_text(moves[i])}")
        for i in range(len(boards)):
            print(F"{i + 1} => {StateParser.convert_board_to_text(boards[i])}")

    @staticmethod
    def generate(board: Board, moves: List[Move]) -> List[Board]:
        """
        Applies every move in a list of moves to a board and gets a list of resulting boards.
        :return: List of resulting boards for each move.
        """
        boards = [Board.create_from_data(board.to_array()) for _ in range(len(moves))]
        for i in range(len(moves)):
            boards[i].apply_move(moves[i])

        return boards

    @classmethod
    def enumerate_board(cls, board: Board, current_player: Color) -> List[Move]:
        """
        Enumerates through every position on the board and finds every possible unique selection for a player.
        From each selection, iterates through every possible move, finding only valid moves.
        :return: List of valid moves for a board.
        """
        selections = []
        for cell, _ in board.enumerate():
            if board.cell_owned_by(cell, current_player):
                possible_selections = cls._get_possible_selections(board, cell, current_player)
                selections.extend([selection for selection in possible_selections if selection not in selections])

        moves = []
        for possible_selection in selections:
            moves.extend(cls._get_valid_moves(board, possible_selection, current_player))

        return moves

    @staticmethod
    def _get_possible_selections(board: Board, origin_cell: Hex, current_player: Color) -> List[Selection]:
        """
        Gets every possible selection from a cell of origin on the board.
        :return: List of selections from an origin cell.
        """
        selections = [
            Selection(origin_cell)
        ]

        for direction in HexDirection:
            next_cell = origin_cell
            for i in range(Selection.MAX_SIZE - 1):
                next_cell = Hex.add(next_cell, direction.value)

                if not board.cell_owned_by(next_cell, current_player):
                    break

                selections.append(Selection(origin_cell, next_cell))

        return selections

    @staticmethod
    def _get_valid_moves(board: Board, selection: Selection, current_player: Color) -> List[Move]:
        """
        Iterates through a move in every direction from a selection on the board and filters for valid moves.
        :return: List of valid moves from given selection.
        """
        moves = [Move(selection, direction) for direction in HexDirection]
        return [move for move in moves if board.is_valid_move(move, current_player)]
