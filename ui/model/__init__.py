from dataclasses import dataclass, field

from core.game import Game
from core.hex import HexDirection
from core.selection import Selection
from core.move import Move
from core.constants import MAX_SELECTION_SIZE

from ui.model.config import Config
from ui.model.game_history import GameHistory

@dataclass
class Model:
    selection: Selection = None
    paused: bool = False
    game: Game = field(default_factory=Game)
    history: GameHistory = field(default_factory=GameHistory)
    config: Config = field(default_factory=lambda: Config.from_default())

    @property
    def game_board(self):
        return self.game.board

    @property
    def game_turn(self):
        return self.game.turn

    def select_cell(self, cell):
        selection = self.selection
        selection_head = selection and (selection.end or selection.start)

        if not selection:
            if cell in self.game_board and self.game_board[cell] == self.game_turn:
                self.selection = Selection(start=cell, end=cell)
            return None

        if cell not in self.game_board:
            self.selection = None
            return None

        if self.game_board[cell] == self.game_turn:
            selection.start = selection.end or selection.start
            selection.end = cell
            selection_cells = selection.to_array()
            selection_color = selection.get_player(self.game_board)
            if (not selection_cells
            or len(selection_cells) > MAX_SELECTION_SIZE
            or next((True for c in selection_cells
                if self.game_board[c] != selection_color), False)):
                self.selection = None
            return None

        elif selection_head.adjacent(cell):
            normal = cell.subtract(selection_head)
            direction = HexDirection.resolve(normal)
            move = Move(selection, direction)
            if self.game_board.is_valid_move(move, self.game_turn.value): # TODO: use color enum
                return move

        self.selection = None
        return None # explicit None return for consistency

    def apply_move(self, move):
        self.selection = None
        if self.game.apply_move(move):
            return move

    def apply_config(self, config):
        self.game = Game(config.layout)
