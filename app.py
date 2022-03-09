from core.game import Game
from ui.game_ui import GameUI
from ui import settings_ui
from tkinter import Tk


class App:
    """
    The App class is the driver of the program and contains the functions of the program.
    """
    WIDTH = 800
    HEIGHT = 600
    DIMENSIONS = F"{WIDTH}x{HEIGHT}"

    def __init__(self):
        self.root = Tk()
        self.game = Game()
        self.settings = settings_ui.SettingsUI()

    def run_game(self):
        """
        Main driver of the program.
        :return: none
        """
        self.display_game()
        self.root.title(Game.TITLE)
        self.root.geometry(self.DIMENSIONS)
        self.root.configure(background=GameUI.COLOR_BACKGROUND_PRIMARY)
        self.root.mainloop()

    def display_game(self):
        """
        Displays the GUI.
        :return: none
        """
        self.game.display(self.root, handle_open_settings=self.open_settings)

    def open_settings(self):
        """
        Displays a settings pop up for user customization input.
        :return: none
        """
        settings_window = Tk()
        settings_window.title(settings_ui.SettingsUI.TITLE)
        self.settings.display(settings_window,
                              handle_confirm=lambda config: self.confirm_settings(settings_window, config))

    def confirm_settings(self, window, config):
        """
        Creates a new game with the specified settings.
        :param window: window
        :param config: config
        :return: none
        """
        self.game.update_settings(config)
        self.display_game()  # Redraw Game Window
        window.destroy()  # Destroy Settings Window


if __name__ == "__main__":
    app = App()
    app.run_game()
