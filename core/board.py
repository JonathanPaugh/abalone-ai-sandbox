"""
Contains Abalone-specific hex grid logic.
"""

from __future__ import annotations

from core.constants import BOARD_SIZE
from core.selection import Selection
from core.move import Move
from core.color import Color
from core.hex import Hex
from lib.hex.hex_grid import HexGrid


class Board(HexGrid):
    """
    A hex grid specific to the game of Abalone.
    Implements serialization, extra iteration helpers, and a reference to
    starting layout data for headlessly calculating game score.
    """

    MAX_SUMITO = 3

    @staticmethod
    def create_from_data(data: list[list[int]]):
        """
        Creates a board from the given board data.
        The original board data is cached within the board for score calculations.
        :param data: an array of arrays of domain 0..2
        :return: a Board
        """
        board = Board()
        board._layout = data
        for r, line in enumerate(data):
            for q, val in enumerate(line):
                q += board.offset(r)  # offset coords - board storage starts at x with size - 1
                cell = Hex(q, r)
                try:
                    board[cell] = Color(val)
                except ValueError:
                    board[cell] = None
        return board

    def __init__(self):
        """
        Initializes a game board.
        """
        super().__init__(size=BOARD_SIZE)
        self._layout = None
        self.__items = None
        self.__items_dirty = None
        self.__items_nonempty = None

    @property
    def layout(self) -> list[list[int]]:
        """
        Gets the board's starting layout.
        Used for headlessly calculating game score.
        """
        return self._layout

    def enumerate(self) -> list[tuple[Hex, Color]]:
        """
        Returns all positions and values on the game board a la `enumerate`.
        :return: a list of (Hex, Color) tuples
        """
        if not self.__items:
            items = []
            for r, line in enumerate(self._data):
                for q, val in enumerate(line):
                    q += self.offset(r)
                    item = (Hex(q, r), val)
                    items.append(item)
            self.__items = items

        if self.__items_dirty:
            self.__items_dirty = False
            items = self.__items
            i = 0
            for r, line in enumerate(self._data):
                for q, val in enumerate(line):
                    q += self.offset(r)
                    item = (Hex(q, r), val)
                    items[i] = item
                    i += 1

        return self.__items

    def enumerate_nonempty(self) -> list[tuple[Hex, Color]]:
        """
        Enumerates all non-empty (cell, value) pairs.
        :return: a list of (Hex, Color) tuples
        """
        if not self.__items_nonempty:
            items = []
            for r, line in enumerate(self._data):
                for q, val in enumerate(line):
                    if val is None:
                        continue
                    q += self.offset(r)
                    item = (Hex(q, r), val)
                    items.append(item)
            self.__items_nonempty = items
        return self.__items_nonempty

    def cell_in_bounds(self, cell: Hex) -> bool:
        """
        :return: If the cell is in bounds.
        """
        return cell in self

    def cell_owned_by(self, cell: Hex, player: Color) -> bool:
        """
        :return: If the cell is owned by the player.
        """
        return self.cell_in_bounds(cell) and self[cell] and self[cell] == player

    def is_valid_move(self, move: Move, current_player: Color) -> bool:
        """
        :return: If the move is valid.
        """
        if move.is_single():
            return self._is_valid_single_move(move)

        if move.is_inline():
            return self._is_valid_inline_move(move, current_player)

        return self._is_valid_sidestep_move(move)

    def get_marble_count(self, player: Color) -> int:
        """
        :return: Marble count for player.
        """
        count = 0
        for _, color in self.enumerate():
            if color == player:
                count += 1

        return count

    def get_score(self, player: Color) -> int:
        """
        :return: Score for player.
        """
        opponent = Color.next(player)

        layout_count = 0
        for line in self._layout:
            for data in line:
                if data == opponent.value:
                    layout_count += 1

        return layout_count - self.get_marble_count(opponent)

    def get_scores_optimized(self, player: Color, player_count: int, opponent_count: int) -> tuple[int, int]:
        """
        :param player: The player.
        :param player_count: Player marble count.
        :param opponent_count: Opponent marble count.
        :return: Score for player and opponent player.
        """
        opponent = Color.next(player)

        player_layout_count = 0
        opponent_layout_count = 0
        for line in self._layout:
            for data in line:
                if data == player.value:
                    player_layout_count += 1
                if data == opponent.value:
                    opponent_layout_count += 1

        return opponent_layout_count - opponent_count, player_layout_count - player_count

    def apply_move(self, move: Move):
        """
        Applies a move to the board, changing the position of cells.
        """
        self._apply_sumito_move(move) if move.is_sumito(self) else self._apply_base_move(move)

    def _is_valid_single_move(self, move: Move) -> bool:
        """
        :return: Is a valid single cell move.
        :precondition: Selection is a single cell.
        """
        destination = move.selection.start.add(move.direction.value)

        if not self.cell_in_bounds(destination):
            return False

        if self[destination]:
            return False

        return True

    def _is_valid_inline_move(self, move: Move, current_player: Color) -> bool:
        """
        :return: Is a valid inline move.
        :precondition: Move is inline.
        """
        destination = move.get_front()
        out_of_bounds_valid = False
        for i in range(1, self.MAX_SUMITO + 1):
            destination = destination.add(move.direction.value)
            if not self.cell_in_bounds(destination):
                return out_of_bounds_valid
            if not self[destination]:
                return True
            if self[destination] == current_player:
                return False
            else:
                if i >= move.selection.get_size():
                    return False

                out_of_bounds_valid = True

        return True

    def _is_valid_sidestep_move(self, move: Move) -> bool:
        """
        :return: Is a valid sidestep move.
        :precondition: Move is sidestep.
        """
        for cell in move.selection.to_array():
            destination = cell.add(move.direction.value)

            if not self.cell_in_bounds(destination):
                return False

            if self[destination]:
                return False

        return True

    def _apply_base_move(self, move: Move):
        """
        Applies a move to the board, moving cells at origin to destination.
        :precondition: Move is not sumito.
        """
        player = move.selection.get_player(self)

        for cell in move.selection.to_array():
            self[cell] = None

        for cell in move.get_destinations():
            self[cell] = player

    def select_marbles_in_line(self, start, direction):
        """
        Selects all marbles in the line specified by the given start and direction.
        Selection ends when the destination goes out of bounds or highlights a new color.
        :param start: the Hex to start selecting from
        :param direction: the HexDirection to select in
        :return: a Selection
        """

        color = self[start]
        if color == None:
            return None

        dest_cell = start
        next_cell = start
        while next_cell in self and self[next_cell] == color:
            dest_cell = next_cell
            next_cell = next_cell.add(direction.value)

        return Selection(start, Hex(dest_cell.x, dest_cell.y))

    def _apply_sumito_move(self, move: Move):
        """
        Applies a sumito move to the board, first moves blocking cells in the direction of the move,
        then applies the base move after.
        :precondition: Move is sumito.
        """
        sumito_selection = self.select_marbles_in_line(
            start=move.get_front().add(move.direction.value),
            direction=move.direction,
        )
        sumito_move = Move(sumito_selection, move.direction)

        player = sumito_move.selection.get_player(self)

        for cell in sumito_move.selection.to_array():
            if self.cell_in_bounds(cell):
                self[cell] = None

        for cell in sumito_move.get_destinations():
            if self.cell_in_bounds(cell):
                self[cell] = player

        self._apply_base_move(move)

    def __str__(self):
        # TODO: return a list of comma-separated "pieces", e.g. A1w
        return super().__str__()

    def __setitem__(self, cell, value):
        """
        Sets the value on the board at position `cell` to `value`.
        :param cell: a Hex
        :param value: the value to set
        """
        super().__setitem__(cell, value)
        if cell in self:
            # mark enumeration struct as in need of recalculation

            # TODO(B): only change the value for the associated item
            # how to reliably generate a linear index for an item by cell?
            # most likely isn't possible for non-empty cells without linear
            # search -- though still more performant than regenerating the
            # entire board cache
            self.__items_dirty = True

            # TODO(B): possible mem optimization -- use dirty flag here as well
            # length of nonempty sequence can be determined by current length
            # plus delta (+1 if `None`->`not None`, -1 if `not None`->`None`)
            self.__items_nonempty = None

    def copy_state(self, board):
        data = self._data
        for r, line in enumerate(board._data):
            for q, val in enumerate(line):
                data[r][q] = val
        self.__items = None
        self.__items_nonempty = None
