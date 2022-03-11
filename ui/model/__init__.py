from dataclasses import dataclass, field
from core.game import Game
from core.hex import HexDirection
from core.selection import Selection
from core.move import Move
from ui.config import Config
from ui.game_history import GameHistory


def is_move_target_empty(board, move):
    move_dests = move.get_destinations()
    selection_cells = move.selection.to_array()
    return next((False for dest in move_dests
        if dest not in selection_cells and board[dest] is not None), True)


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
            selection_head = selection.end or selection.start
            if selection_head.adjacent(cell):
                normal = cell.subtract(selection_head)
                direction = HexDirection.resolve(normal)
                move = Move(selection, direction)
                if is_move_target_empty(self.game_board, move):
                    return self.apply_selection(move)
            self.selection = None

        else:
            selection.start = selection.end or selection.start
            selection.end = cell
            selection_cells = selection.to_array()
            selection_color = selection.get_player(self.game_board)
            if (not selection_cells
            or next((True for c in selection_cells
                if self.game_board[c] != selection_color), False)):
                self.selection = None

    def apply_selection(self, move):
        self.game_board.apply_move(move)
        self.selection = None
        return move

    def apply_config(self, config):
        self.game = Game(config.layout)
