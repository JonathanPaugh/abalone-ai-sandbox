from tkinter import Tk
from ui.view.game import GameUI
from ui.view.settings import SettingsUI

class View:
    TITLE = "Abalone"

    def __init__(self):
        self._window = Tk()
        self._game_ui = GameUI()
        self._settings_ui = SettingsUI()

    @property
    def window(self):
        return self._window

    def open(self):
        self._window.title(View.TITLE)
        self._window.configure(background=GameUI.COLOR_BACKGROUND_PRIMARY)

    def display_board(self, parent, board, handle_open_settings):
        self._game_ui.display(parent, board, handle_open_settings)

    def open_settings(self):
        """
        Displays a settings pop up for user customization input.
        :return: none
        """
        settings_window = Tk()
        settings_window.title(SettingsUI.TITLE)
        self._settings_ui.display(settings_window,
                                  handle_confirm=lambda config: self.confirm_settings(settings_window, config))

    def confirm_settings(self, window, config):
        """
        Creates a new game with the specified settings.
        :param window: window
        :param config: config
        :return: none
        """
        window.destroy()  # Destroy Settings Window
