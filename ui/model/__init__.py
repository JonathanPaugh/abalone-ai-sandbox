"""
Defines the model for the application.
"""

from dataclasses import dataclass, field

from core.game import Game
from core.hex import HexDirection
from core.selection import Selection
from core.move import Move
from core.constants import MAX_SELECTION_SIZE

from ui.model.config import Config
from ui.model.game_history import GameHistory


@dataclass # TODO(?): un-dataclass for field privacy
class Model:
    """
    The model for the application.
    Contains view-agnostic application state.
    """

    selection: Selection = None
    paused: bool = False
    game: Game = field(default_factory=Game)
    history: GameHistory = field(default_factory=GameHistory)
    config: Config = field(default_factory=Config.from_default)

    @property
    def game_board(self):
        """
        Gets the game board.
        :return: a Board
        """
        return self.game.board

    @property
    def game_turn(self):
        """
        Gets the color indicating whose turn it is.
        :return: a Color
        """
        return self.game.turn

    @property
    def game_config(self):
        """
        Gets the config of the game.
        :return: a Config
        """
        return self.config

    def select_cell(self, cell):
        """
        Selects the given cell.
        :param: the Hex to select
        :return: the Move to perform if applicable, else None
        """

        selection = self.selection
        selection_head = selection and (selection.end or selection.start) # TODO(?): add head method

        # select marbles corresponding to the current turn
        if not selection:
            if cell in self.game_board and self.game_board[cell] == self.game_turn:
                self.selection = Selection(start=cell, end=cell)
            return None

        # deselect if out of bounds
        if cell not in self.game_board:
            self.selection = None
            return None

        # select new end cell if possible
        if self.game_board[cell] == self.game_turn:
            selection.start = selection.end or selection.start
            selection.end = cell
            selection_cells = selection.to_array()
            selection_color = selection.get_player(self.game_board)
            if (not selection_cells # TODO: Selection.is_valid_selection(board)?
            or len(selection_cells) > MAX_SELECTION_SIZE
            or next((True for c in selection_cells
                if self.game_board[c] != selection_color), False)):
                self.selection = None
            return None

        # perform move if cell is adjacent to last clicked cell
        if selection_head.adjacent(cell):
            normal = cell.subtract(selection_head)
            direction = HexDirection.resolve(normal)
            move = Move(selection, direction)
            if self.game_board.is_valid_move(move, self.game_turn.value): # TODO: use color enum
                return move

        self.selection = None
        return None # consistency

    def apply_move(self, move):
        """
        Applies the given move to the game board.
        :param move: the move to apply
        :return: None
        """
        self.game.apply_move(move)
        self.selection = None

    def apply_config(self, config):
        """
        Applies the given config and starts a new game.
        :param config: the new Config to use
        :return: None
        """
        self.config = config
        self.game = Game(config.layout)
