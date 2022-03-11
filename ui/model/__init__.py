from dataclasses import dataclass, field
from core.game import Game
from core.selection import Selection
from ui.config import Config
from ui.game_history import GameHistory

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

    def select_cell(self, cell):
        selection = self.selection

        if not selection:
            self.selection = Selection(start=cell, end=cell)

        elif selection and cell not in self.game_board:
            self.selection = None

        elif selection and self.game_board[cell] is None:
            self.selection = None

        else:
            selection.start = selection.end or selection.start
            selection.end = cell
            if not selection.to_array():
                self.selection = None

    def apply_config(self, config):
        self.game = Game(config.layout)
