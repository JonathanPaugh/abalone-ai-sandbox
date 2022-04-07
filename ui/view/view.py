"""
Defines the view for the application.
"""

from tkinter import Tk
from ui.view.game import GameUI
from ui.view.settings import SettingsUI
from ui.constants import APP_NAME
from datetime import timedelta


class View:
    """
    The view for the application.
    Receives callbacks for user-initiated events via `open` (for windows) and
    `mount` methods (for other widgets), and receives application state via
    `render` methods (for implicit updates) and actions (for explicit updates).
    """

    def __init__(self):
        self._window = None
        self._done = False
        self._game_view = GameUI()
        self._settings_view = None

    @property
    def window(self):
        """
        Gets the window for the application.
        :return: a Tk instance
        """
        return self._window

    @property
    def done(self):
        """
        Gets whether or not the application has been closed.
        :return: a bool
        """
        return self._done

    @property
    def animating(self):
        """
        Determines whether or not the view is being animated.
        :return: a bool
        """
        return self._game_view.animating

    def _open_settings(self, config, on_close):
        """
        Displays a settings pop up for user customization input.
        :return: none
        """
        self._settings_view = SettingsUI(config, on_close=lambda config: self._close_settings(config, on_close)).open()

    def _close_settings(self, config, on_close):
        self._settings_view = None
        if on_close and config:
            on_close(config)

    def open(self, on_exit, get_config, can_open_settings, on_open_settings, on_confirm_settings, **kwargs):
        """
        Opens the view window.
        Mounts child widgets and binds event handlers.
        :return: None
        """

        self._window = Tk()
        self._window.title(APP_NAME)
        self._window.configure(background=GameUI.COLOR_BACKGROUND_PRIMARY)
        self._window.protocol("WM_DELETE_WINDOW", lambda: (
            on_exit(),
            setattr(self, "_done", True)
        ))

        self._game_view.mount(self._window,
            on_click_settings=lambda: (
                not self._settings_view and can_open_settings()
                and (self._open_settings(get_config(), on_close=on_confirm_settings) or on_open_settings())
            ),
            **kwargs
        )

    def update(self):
        """
        Performs per-frame view updates.
        :return: None
        """
        self._window.update()
        self._game_view.update()

    def update_timer(self, time: timedelta):
        """
        Preforms a lightweight update to only the game view timer.
        :param time: a time to display.
        """
        self._game_view.update_timer(time)

    def render(self, model):
        """
        Diffs the given model against view state and queues up changes to
        display on update.
        :param model: the model to render
        :return: None
        """
        self._game_view.render(model)

    def clear_game_board(self):
        """
        Clears the entire game board.
        :return: None
        """
        self._game_view.clear_board()

    def apply_move(self, *args, **kwargs):
        """
        Visually moves the marbles affected by the given move.
        :param *args, **kwargs: the action parameters
        :return: None
        """
        self._game_view.apply_move(*args, **kwargs)

    def apply_config(self, config):
        self._game_view.apply_config(config)
