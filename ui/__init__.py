from time import sleep

from ui.model import Model
from ui.view import View
from ui.constants import FPS


class App:
    """
    The App class is the driver of the program and contains the functions of the program.
    """

    def __init__(self):
        self._model = Model()
        self._view = View()

    def _dispatch(self, action, *args, **kwargs):
        action(*args, **kwargs)
        self._view.render(self._model)

    def _select_cell(self, cell):
        move = self._model.select_cell(cell)
        move and self._apply_move(move)

    def _apply_move(self, move):
        self._view.apply_move(move, board=self._model.game_board)
        self._model.apply_move(move)

        # STUB(agent): if model config's control mode for the current player is
        # the CPU, call procedure for running agent and applying resulting move

    def _update(self):
        # STUB(agent): async agent move requests may be called from here
        self._view.update()

    def _run_main_loop(self):
        while not self._view.closed:
            self._update()
            sleep(1 / FPS)

    def run_game(self):
        """
        Main driver of the program.
        :return: none
        """
        self._view.open(
            on_click_board=lambda cell: (
                self._dispatch(self._select_cell, cell),
            ),
            on_confirm_settings=lambda config: (
                self._dispatch(self._model.apply_config, config),
            ),
            # STUB: this should go through an `askokcancel` if game is running
            can_open_settings=lambda: True,
        )
        self._view.render(self._model)
        self._run_main_loop()
