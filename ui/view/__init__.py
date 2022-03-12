from tkinter import Tk
from ui.view.game import GameUI
from ui.view.settings import SettingsUI

class View:
    TITLE = "Abalone"

    def __init__(self):
        self._window = None
        self._closed = False
        self._game_view = GameUI()
        self._settings_view = None

    @property
    def window(self):
        return self._window

    @property
    def closed(self):
        return self._closed

    def open(self, on_click_board, can_open_settings, on_confirm_settings):
        self._window = Tk()
        self._window.title(View.TITLE)
        self._window.configure(background=GameUI.COLOR_BACKGROUND_PRIMARY)
        self._window.protocol("WM_DELETE_WINDOW", lambda: (
            setattr(self, "_closed", True)
        ))

        self._game_view.display(self._window,
            on_click_board=on_click_board,
            on_click_settings=lambda: (
                not self._settings_view and can_open_settings()
                    and self.open_settings(on_close=on_confirm_settings)
            ),
        )

    def open_settings(self, on_close):
        """
        Displays a settings pop up for user customization input.
        :return: none
        """
        self._settings_view = SettingsUI(on_close=lambda config: (
            setattr(self, "_settings_view", None),
            on_close and on_close(config),
        )).open()

    def update(self):
        self._window.update()
        self._game_view.update()

    def render(self, model):
        self._game_view.render(model)

    def apply_move(self, *args, **kwargs):
        self._game_view.apply_move(*args, **kwargs)
