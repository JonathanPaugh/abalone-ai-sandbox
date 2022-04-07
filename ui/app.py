"""
Defines the driver logic for the application.
"""
from __future__ import annotations
from typing import TYPE_CHECKING

from datetime import timedelta
from time import sleep
import json
import os
import sys

from agent.heuristics.heuristic_jonathan import Heuristic
from agent.state_generator import StateGenerator
from agent.ponderer import PonderingAgent
from core.color import Color
from core.move import Move
from core.player_type import PlayerType
from core.board_layout import BoardLayout
from lib.dispatcher import Dispatcher
from ui.model.game_history import GameHistory
from ui.model.model import Model, GameHistoryItem
from ui.model.config import Config
from ui.view import View
from ui.debug import Debug, DebugType
from ui.constants import FPS, DEBUG_FILEPATH

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
        self._agents = {}
        self._update_dispatcher = Dispatcher()
        self.paused = False
        self.allow_move = True

    def _start_game(self):
        """
        Starts the game by applying a random move to the first player.
        """
        config = self._model.config

        self._agents = {
            Color.BLACK: config.agent_type_p1.create() if config.player_type_p1 is PlayerType.COMPUTER else None,
            Color.WHITE: config.agent_type_p2.create() if config.player_type_p2 is PlayerType.COMPUTER else None,
        }

        self._apply_heuristic_config(config)
        if config.get_player_type(self._model.game_turn) == PlayerType.COMPUTER:
            self._apply_random_move()

    def _stop_game(self):
        if self.paused:
            self._set_pause(False)
        self._model.stop_timer()
        self._stop_agents()
        self._update_dispatcher.clear()

    def _set_pause(self, pause: bool):
        pause != self.paused and self._toggle_pause()

    def _toggle_pause(self):
        self.paused = not self.paused
        self._model.toggle_pause()
        self._toggle_agents_paused()
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

        time_p1 = self._model.history.get_player_total_time(Color.BLACK)
        time_p2 = self._model.history.get_player_total_time(Color.WHITE)

        if time_p1 < time_p2:
            print(F"{Color.BLACK} has the best aggregate time: {time_p1:.2f} seconds")
        elif time_p2 < time_p1:
            print(F"{Color.WHITE} has the best aggregate time: {time_p2:.2f} seconds")

    def _set_timeout_move(self, move: Move):
        """
        Sets the timeout move for current player.
        """
        self._model.timeout_move = move

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

    def _advance_turn(self):
        """
        Advances the game to the next player and starts the agent if the player is a computer.
        :return:
        """
        Debug.log(F"--- Next Turn: {self._model.game_turn} ---", DebugType.Game)

        if not self._model.next_turn(lambda progress: self._update_dispatcher.put(lambda: self._update_timer(progress)),
                                     lambda: self._update_dispatcher.put(self._apply_timeout_move),
                                     self.end_game):
            self.allow_move = True
            return

        if self._model.config.get_player_type(self._model.game_turn) is PlayerType.COMPUTER:
            self._process_agent_move()

        self.allow_move = True
        self._start_pondering()

    def _process_agent_move(self):
        """
        Hands control over to the agent to perform a move if the player to move
        is CPU-controlled.
        :return: None
        """
        config = self._model.game_config
        player_color = self._model.game_turn

        player_type = config.get_player_type(player_color)
        if player_type is not PlayerType.COMPUTER:
            return

        agent = self._agents[player_color]
        agent_move = (agent.get_refutation_move(self._model.game_board)
            if isinstance(agent, PonderingAgent)
            else None)  # can we assume that every agent has a refutation table?

        if agent_move:
            self._update_dispatcher.put(lambda: self._apply_move(agent_move))
            return

        agent.start(self._model.game_board,
                    player_color,
                    self._set_timeout_move,
                    lambda: self._update_dispatcher.put(self._apply_timeout_move))

    def _start_pondering(self):
        config = self._model.game_config
        player_color = self._model.game_turn
        next_player_color = Color.next(self._model.game_turn)

        next_player_type = config.get_player_type(next_player_color)
        if next_player_type is not PlayerType.COMPUTER:
            return

        next_agent = self._agents[next_player_color]
        if next_agent.is_searching or not isinstance(next_agent, PonderingAgent):
            return

        next_agent.ponder(board=self._model.game_board, player=player_color)

    def _apply_move(self, move: Move):
        """
        Applies the given move to the game board, updating both the model and view accordingly.
        :param move: the Move to apply
        :return: None
        """
        if not self.allow_move:
            return

        self.allow_move = False

        self._notify_agents(move)

        if not move:
            Debug.log(F"Warning: Apply move called with empty move, generating random move",
                            DebugType.Warning)

            move = StateGenerator.generate_random_move(self._model.game_board, self._model.game_turn)

        Debug.log(F"Apply Move: {move}, {self._model.game_turn}", DebugType.Game)

        self._view.apply_move(move,
                              board=self._model.game_board,
                              on_end=lambda: self._update_dispatcher.put(self._advance_turn))
        self._model.apply_move(move)
        self._update_dispatcher.put(lambda: self._view.render(self._model))

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
        self._stop_agents()
        self._apply_move(self._model.timeout_move)

    def _apply_config(self, config: Config):
        """
        Applies the given config and starts a new game.
        :param config: the new Config to use
        :return: None
        """
        self._model.apply_config(config)
        self._reset_game()
        self._apply_heuristic_config(config)
        self._view.render(self._model)

    def _apply_heuristic_config(self, config: Config = None):
        config = config or self._model.game_config
        for color, agent in self._agents.items():
            if agent:
                agent.set_heuristic_type(config.get_player_heuristic_type(color))

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

    def _update_timer(self, time_remaining: float):
        """
        Queues a time to render to timer on the next update frame.
        :param time: a float in seconds
        """
        time = timedelta(seconds=time_remaining)
        self._view.update_timer(time)

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
        self._read_history_dump()

        Heuristic.set_turn_count_handler(lambda: self._model.get_turn_count(self._model.game_turn))
        self._view.open(
            get_config=lambda: self._model.config,
            on_exit=self._stop_game,
            can_open_settings=lambda: True,  # STUB: this should go through an `askokcancel` if game is running
            on_open_settings=lambda: (
                self._dispatch(self._set_pause, True),
            ),
            on_confirm_settings=lambda config: (
                self._update_dispatcher.put(lambda: self._dispatch(self._apply_config, config)),
                self._dispatch(self._set_pause, False),
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
                self._dispatch(self.end_game),
            ),
            on_click_reset=self._reset_game,
        )
        self._view.render(self._model)

        try:
            self._start_game()
            self._run_main_loop()
            self._stop_agents()
        finally:
            self._write_history_dump()

    def _stop_agents(self):
        self._rally_agents(lambda agent: agent.stop())

    def _notify_agents(self, move):
        self._rally_agents(lambda agent: agent.apply_move(move))

    def _toggle_agents_paused(self):
        self._rally_agents(lambda agent: agent.toggle_paused())

    def _rally_agents(self, callback: callable):
        """
        Performs `callback` on all agents.
        """
        for agent in self._agents.values():
            if agent:
                callback(agent)

    def _read_history_dump(self):
        try:
            with open(DEBUG_FILEPATH, mode="r", encoding="utf-8") as file:
                file_buffer = file.read()
        except FileNotFoundError:
            return

        try:
            starting_layout_str, game_history_str = json.loads(file_buffer)
            starting_layout = BoardLayout[starting_layout_str]
            game_history = GameHistory.decode(game_history_str)
        except Exception:
            Debug.log(sys.exc_info(), DebugType.Warning)
            Debug.log(f"WARNING: {DEBUG_FILEPATH} is corrupted, removing...", DebugType.Warning)
            os.remove(DEBUG_FILEPATH)  # remove corrupted file

        # self._model.apply_history(history)

    def _write_history_dump(self):
        starting_layout = self._model.config.layout.name
        game_history = self._model.history
        file_buffer = json.dumps([starting_layout, str(game_history)], separators=(",", ":"))
        with open(DEBUG_FILEPATH, mode="w", encoding="utf-8") as file:
            file.write(file_buffer)
