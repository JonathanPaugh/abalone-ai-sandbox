from math import sqrt
from lib.hex.transpose_hex import point_to_hex

from core.hex import Hex
from ui.model import Model
from ui.view import View
from core.constants import BOARD_CELL_SIZE, BOARD_SIZE, BOARD_MAX_COLS

class App:
    """
    The App class is the driver of the program and contains the functions of the program.
    """

    def __init__(self):
        self._model = Model()
        self._view = View()

    def run_game(self):
        """
        Main driver of the program.
        :return: none
        """
        self._view.open(
            on_click_board=lambda pos: (
                hex_xradius := BOARD_CELL_SIZE / 2,
                hex_yradius := BOARD_CELL_SIZE / sqrt(3),
                x := pos[0] - hex_xradius - (BOARD_MAX_COLS - BOARD_SIZE) * hex_xradius,
                y := pos[1] - hex_xradius,
                cell := point_to_hex((x, y), hex_yradius),
                hex := Hex(cell[0] + BOARD_MAX_COLS // 2, cell[1]),
                self._select_cell(hex),
            ),
            can_open_settings=lambda: True,
            on_confirm_settings=lambda config: (
                self._model.apply_config(config),
                self._view.render(self._model),
            ),
        )
        self._view.render(self._model)

        while not self._view.closed:
            self._view.update()

    def _select_cell(self, cell):
        self._model.select_cell(cell)
        self._view.render(self._model)
