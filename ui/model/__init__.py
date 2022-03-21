"""
Defines the model for the application.
"""
from dataclasses import dataclass, field
from core.game import Game
from core.hex import HexDirection
from core.selection import Selection
from core.move import Move
from lib.interval_timer import IntervalTimer
from ui.model.game_history import GameHistory
from datetime import time, timedelta
import ui.constants

@dataclass # TODO(?): un-dataclass for field rivacy
class Model:
    """
    The model for the application.
    Contains view-agnostic application state.
    """

    selection: Selection = None
    paused: bool = False
    timer: IntervalTimer = None
    history: GameHistory = field(default_factory=GameHistory)
    game: Game = field(default_factory=Game)

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
        return self.game.config

    def select_cell(self, cell):
        """
        Selects the given cell.
        :param: the Hex to select
        :return: the Move to perform if applicable, else None
        """

        selection = self.selection
        selection_head = selection and selection.get_head()

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
            if (selection.is_valid_selection(self.game_board)):
                self.selection = None
            return None

        # perform move if cell is adjacent to last clicked cell
        if selection_head.adjacent(cell):
            normal = cell.subtract(selection_head)
            direction = HexDirection.resolve(normal)
            move = Move(selection, direction)
            if self.game_board.is_valid_move(move, self.game_turn):
                return move

        self.selection = None
        return None # consistency

    def apply_config(self, config):
        """
        Applies the given config and starts a new game.
        :param config: the new Config to use
        :return: None
        """
        self.config = config
        self.game = Game(config)

    def apply_move(self, move, on_timer, on_timeout):
        """
        Applies the given move to the game board.
        :param move: the move to apply
        :return: None
        """
        self.game.apply_move(move)
        self.selection = None
        self._timer_launch(on_timer, on_timeout)

    def _timer_launch(self, on_timer, on_timeout):
        if self.timer:
            self.timer.stop()

        time_limit = self.game_config.get_player_time_limit(self.game_turn)

        self.timer = IntervalTimer(time_limit, float(1 / ui.constants.FPS))
        self.timer.set_on_interval(lambda progress: self._timer_on_interval(on_timer, progress))
        self.timer.set_on_complete(on_timeout)
        self.timer.start()

    def _timer_on_interval(self, on_timer, progress: float) -> time:
        time_remaining = self.timer.total_time * progress
        on_timer(time_remaining)
