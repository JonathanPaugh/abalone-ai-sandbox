"""
Defines the model for the application.
"""
from __future__ import annotations
from typing import TYPE_CHECKING

from dataclasses import dataclass, field

from agent.state_generator import StateGenerator
from core.game import Game
from core.move import Move
from core.hex import HexDirection
from core.player_type import PlayerType
from core.selection import Selection
from lib.interval_timer import IntervalTimer
from ui.model.config import Config
from ui.model.game_history import GameHistory

from datetime import time
from ui.constants import FPS

if TYPE_CHECKING:
    from core.hex import Hex

@dataclass  # TODO(?): un-dataclass for field privacy
class Model:
    """
    The model for the application.
    Contains view-agnostic application state.
    """

    paused: bool = False
    selection: Selection = None
    timer: IntervalTimer = None
    timeout_move: Move = None
    history: GameHistory = field(default_factory=GameHistory)
    game: Game = field(default_factory=Game)
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

    def select_cell(self, cell: Hex):
        """
        Selects the given cell.
        :param: the Hex to select
        :return: the Move to perform if applicable, else None
        """

        selection = self.selection
        selection_head = selection and selection.get_head()

        # disallow selection if is computer
        if self.config.get_player_type(self.game_turn) is PlayerType.COMPUTER:
            self.selection = None
            return None

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
            if selection.is_valid_selection(self.game_board):
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
        return None  # consistency

    def reset(self):
        if self.timer:
            self.timer.stop()

        self.timeout_move = None
        self.selection = None

        self.game = Game(self.config.layout)

    def apply_config(self, config: Config):
        """
        Applies the given config and starts a new game.
        :param config: the new Config to use
        :return: None
        """
        self.config = config
        self.reset()

    def apply_move(self, move: Move, on_timer: callable, on_timeout: callable):
        """
        Applies the given move to the game board.
        :param move: the move to apply
        :param on_timer: the callable for each timer tick
        :param on_timeout: the callable for when timer is complete
        :return: None
        """
        self.game.apply_move(move)
        self.selection = None
        self._timer_launch(on_timer, on_timeout)

    def _timer_launch(self, on_timer: callable, on_timeout: callable):
        if self.timer:
            self.timer.stop()

        time_limit = self.game_config.get_player_time_limit(self.game_turn)

        self.timer = IntervalTimer(time_limit, 1 / FPS)
        self.timer.set_on_interval(lambda progress: self._timer_on_interval(on_timer, progress))
        self.timer.set_on_complete(lambda: self._timer_on_complete(on_timeout))
        self.timer.start()

    def _timer_on_interval(self, on_timer: callable, progress: float) -> time:
        time_remaining = self.timer.total_time * progress
        on_timer(time_remaining)

    def _timer_on_complete(self, on_timeout: callable):
        if not self.timeout_move:
            self.timeout_move = StateGenerator.generate_random_move(self.game_board, self.game_turn)
        on_timeout()
        self.timeout_move = None

