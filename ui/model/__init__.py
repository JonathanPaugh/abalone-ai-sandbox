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
        pass

    def apply_config(self, config):
        self.game = Game(config.layout)
