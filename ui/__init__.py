"""
Defines the driver logic for the application.
"""
from time import sleep

from agent.agent import Agent
from core.color import Color
from core.player_type import PlayerType
from ui.model import Model
from ui.view import View
from ui.constants import FPS


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

    def _dispatch(self, action, *args, **kwargs):
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

    def _select_cell(self, cell):
        """
        Selects the given cell.
        :param cell: the Hex to select
        :return: None
        """
        move = self._model.select_cell(cell)
        if move:
            self._apply_move(move)

    def _apply_move(self, move):
        """
        Applies the given move to the game board, updating both the model and
        view accordingly.
        :param move: the Move to apply
        :return None:
        """
        self._view.apply_move(move, board=self._model.game_board)
        self._model.apply_move(move)

        config = self._model.config

        player_type = {
            Color.BLACK: config.player_type_p1,
            Color.WHITE: config.player_type_p2
        }[self._model.game_turn]

        if (player_type == PlayerType.COMPUTER):
            next_move = self._agent.find_next_move(self._model.game_board, self._model.game_turn)
            self._apply_move(next_move)

        # STUB(agent): if model config's control mode for the current player is
        # the CPU, call procedure for running agent and applying resulting move
        # TODO: Modify agent to run on separate thread so it can process independently

    def _apply_config(self, config):
        """
        Applies the given config and starts a new game.
        :param config: the new Config to use
        :return: None
        """
        self._model.apply_config(config)
        self._view.clear_game_board()

    def _update(self):
        """
        Updates the application by one tick.
        :return: None
        """
        # STUB(agent): async agent move requests may be called from here
        self._view.update()

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
        self._run_main_loop()
