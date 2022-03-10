from ui.model import Model
from ui.view import View

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
        self._view.open()
        self._view.display_board(self._view.window, self._model.game_board,
            handle_open_settings=self._view.open_settings)
        self._view.window.mainloop()

    def select_cell(self, cell):
        self._model.select_cell(cell)
