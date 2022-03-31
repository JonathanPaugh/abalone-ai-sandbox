"""
Defines the driver logic for the application.
"""
from __future__ import annotations
from typing import TYPE_CHECKING

from datetime import timedelta
from time import sleep

from agent.heuristics.heuristic import Heuristic
from agent.state_generator import StateGenerator
from core.color import Color
from core.move import Move
from core.player_type import PlayerType
from agent.agent import Agent
from lib.dispatcher import Dispatcher
from ui.model import Model, GameHistoryItem
from ui.view import View
from ui.constants import FPS
import ui.model.config as config
import ui.debug

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
        self._agent = Agent()
        self._update_dispatcher = Dispatcher()
        self.paused = False

    def _start_game(self):
        """
        Starts the game by applying a random move to the first player.
        """
        if self._model.config.get_player_type(self._model.game_turn) == PlayerType.COMPUTER:
            self._apply_random_move()

    def end_game(self):
        self._stop_game()

        score_p1 = self._model.game.board.get_score(Color.BLACK)
        score_p2 = self._model.game.board.get_score(Color.WHITE)

        print("Game Over")
        if score_p1 > score_p2:
            print(F"{Color.BLACK} Wins!")
        elif score_p2 > score_p1:
            print(F"{Color.WHITE} Wins!")
        else:
            print("Tie!")

    def _stop_game(self):
        if self.paused:
            self._set_pause(False)
        self._model.stop_timer()
        self._agent.stop()
        self._update_dispatcher.clear()

    def _set_pause(self, pause: bool):
        pause != self.paused and self._toggle_pause()

    def _toggle_pause(self):
        self.paused = not self.paused
        self._model.toggle_pause()
        self._agent.toggle_paused()
        self._view.render(self._model)

    def _undo(self):
        self._stop_game()
        next_item = self._model.undo()
        self._view.clear_game_board()
        self._view.render(self._model)
        self._apply_undo_item(next_item)

    def _reset_game(self):
        self._stop_game()
        self._model.reset()
        self._view.clear_game_board()
        self._view.render(self._model)
        self._start_game()

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
            self._agent.set_heuristic_type(config.get_player_heuristic_type(player_color))
            self._agent.search(self._model.game_board,
                               player_color,
                               self._set_timeout_move,
                               lambda: self._update_dispatcher.put(self._apply_timeout_move))

    def _apply_move(self, move: Move):
        """
        Applies the given move to the game board, updating both the model and
        view accordingly.
        :param move: the Move to apply
        :return: None
        """
        if not move:
            raise Exception("Cannot apply empty move")

        debug.Debug.log(F"Apply Move: {move}, {self._model.game_turn}", debug.DebugType.Game)
        self._view.apply_move(move, board=self._model.game_board, on_end=self._process_agent_move)
        self._model.apply_move(move,
                               self._dispatch_timer_update,
                               lambda: self._update_dispatcher.put(self._apply_timeout_move),
                               self.end_game)
        self._update_dispatcher.put(lambda: self._view.render(self._model))
        debug.Debug.log(F"--- Next Turn: {self._model.game_turn} ---", debug.DebugType.Game)

    def _apply_random_move(self):
        """
        Applies a random move to the game for current player.
        """
        move = StateGenerator.generate_random_move(self._model.game_board, self._model.game_turn)
        self._apply_move(move)

    def _apply_timeout_move(self):
        """
        Applies the currently set timeout move for current player.
        Waits for agent to stop running before applying.
        """
        self._agent.stop()
        self._apply_move(self._model.timeout_move)

    def _set_timeout_move(self, move: Move):
        """
        Sets the timeout move for current player.
        """
        self._model.timeout_move = move

    def _apply_config(self, config: config.Config):
        """
        Applies the given config and starts a new game.
        :param config: the new Config to use
        :return: None
        """
        self._model.apply_config(config)
        self._reset_game()

    def _apply_undo_item(self, item: GameHistoryItem):
        if not item or not item.move:
            self._apply_random_move()
            return
        self._apply_move(item.move)
        self._model.history.pop()
        self._model.history.append(item)

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
        self._update_dispatcher.put(lambda: self._view.update_timer(time))

    def _update(self):
        """
        Updates the application by one tick.
        :return: None
        """
        # STUB(agent): async agent move requests may be called from here
        self._view.update()
        if self.paused:
            return
        self._update_dispatcher.dispatch()

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
        Heuristic.set_turn_count_handler(lambda: self._model.get_turn_count(self._model.game_turn))
        self._view.open(
            get_config=lambda: self._model.config,
            on_exit=self._stop_game,
            can_open_settings=lambda: True,  # STUB: this should go through an `askokcancel` if game is running
            on_open_settings=lambda: (
                self._dispatch(self._set_pause, True),
            ),
            on_confirm_settings=lambda config: (
                self._dispatch(self._apply_config, config),
            ),
            on_click_board=lambda cell: (
                self._dispatch(self._select_cell, cell),
            ),
            on_click_undo=lambda: (
                self._dispatch(self._undo),
            ),
            on_click_pause=lambda: (
                self._dispatch(self._toggle_pause)
            ),
            on_click_stop=lambda: (
                self._dispatch(self._stop_game),
            ),
            on_click_reset=self._reset_game,
        )
        self._view.render(self._model)
        self._start_game()
        self._run_main_loop()
        self._agent.stop()
