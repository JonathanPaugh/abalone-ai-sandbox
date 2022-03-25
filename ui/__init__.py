"""
Defines the driver logic for the application.
"""
from __future__ import annotations
from typing import TYPE_CHECKING

import random
from datetime import timedelta
from time import sleep
from agent.state_generator import StateGenerator
from core.move import Move

from core.player_type import PlayerType
from agent.agent import Agent
from lib.dispatcher import Dispatcher
from ui.model import Model
from ui.view import View
from ui.constants import FPS
import ui.model.config

if TYPE_CHECKING:
    from core.hex import Hex


class App:
    """
    The App is the main driver for the application, and is analogous to the
    Controller in MVC architecture.

    The app retains references to the model and view and is dispatched "actions"
    from the view via centralized event callbacks. Each action triggers a change
    in model state and notifies the view of changes to made to the display.
    """

    def __init__(self):
        self._model = Model()
        self._view = View()
        self._agent_operator = Agent()
        self._view_dispatcher = Dispatcher()

    def _start_game(self):
        """
        Starts the game by applying a random move to the first player.
        """
        self._apply_random_move()

    def _select_cell(self, cell: Hex):
        """
        Selects the given cell.
        :param cell: the Hex to select
        :return: None
        """
        if self._view.animating:
            return

        move = self._model.select_cell(cell)
        if move:
            self._apply_move(move)

    def _process_agent_move(self):
        """
        Hands control over to the agent to perform a move if the player to move
        is CPU-controlled.
        :return: None
        """
        config = self._model.game_config
        player_color = self._model.game_turn
        player_type = config.get_player_type(player_color)

        if player_type is PlayerType.COMPUTER:
            self._agent_operator.search(self._model.game_board,
                                        player_color,
                                        self._set_timeout_move)

    def _apply_move(self, move: Move):
        """
        Applies the given move to the game board, updating both the model and
        view accordingly.
        :param move: the Move to apply
        :return: None
        """
        self._view.apply_move(move, board=self._model.game_board, on_end=self._process_agent_move)
        self._model.apply_move(move, self._dispatch_timer_update, self._apply_timeout_move)

    def _apply_random_move(self):
        move = StateGenerator.generate_random_move(self._model.game_board, self._model.game_turn)
        self._apply_move(move)

    def _apply_timeout_move(self):
        self._agent_operator.stop()
        print(F"Apply: {self._model.timeout_move}")
        self._apply_move(self._model.timeout_move)

    def _set_timeout_move(self, move: Move):
        print(F"Set: {move}")
        self._model.timeout_move = move

    def _apply_config(self, config: ui.Config):
        """
        Applies the given config and starts a new game.
        :param config: the new Config to use
        :return: None
        """
        self._model.apply_config(config)
        self._view.clear_game_board()
        self._view.render(self._model)
        self._agent_operator.stop()
        self._start_game()

    def _dispatch(self, action: callable, *args: list, **kwargs: dict):
        """
        Performs the given action with the given arguments and triggers a view
        re-render.
        :param action: the action to perform
        :return: None
        """
        # TODO: determine whether generic render covers enough of our use cases
        # or if we should just use explicit actions for everything
        action(*args, **kwargs)
        self._view.render(self._model)

    def _dispatch_timer_update(self, time_remaining: float):
        """
        Queues a time to render to timer on the next update frame.
        :param time: a float in seconds
        """
        time = timedelta(seconds=time_remaining)
        self._view_dispatcher.put(lambda: self._view.update_timer(time))

    def _update(self):
        """
        Updates the application by one tick.
        :return: None
        """
        # STUB(agent): async agent move requests may be called from here
        self._view.update()
        self._view_dispatcher.dispatch()

    def _run_main_loop(self):
        """
        Runs the main loop of the application.
        :return: None
        """
        while not self._view.done:
            self._update()
            sleep(1 / FPS)

    def run_game(self):
        """
        Runs the application.
        :return: None
        """
        self._view.open(
            on_click_board=lambda cell: (
                self._dispatch(self._select_cell, cell),
            ),
            on_confirm_settings=lambda config: (
                self._dispatch(self._apply_config, config),
            ),
            # STUB: this should go through an `askokcancel` if game is running
            can_open_settings=lambda: True,
        )
        self._view.render(self._model)
        self._start_game()
        self._run_main_loop()
        self._agent_operator.stop()
