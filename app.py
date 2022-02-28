from game import Game
from game_ui import GameUI
import settings_ui
from tkinter import Tk

class App:
  WIDTH = 800
  HEIGHT = 600
  DIMENSIONS = F"{WIDTH}x{HEIGHT}"

  def __init__(self):
    self.root = Tk()
    self.game = Game()
    self.settings = settings_ui.SettingsUI()

  def run_game(self):
    self.display_game()
    self.root.title(Game.TITLE)
    self.root.geometry(self.DIMENSIONS)
    self.root.attributes('-toolwindow', True)
    self.root.configure(background=GameUI.COLOR_BACKGROUND_PRIMARY)
    self.root.mainloop()

  def display_game(self):
    self.game.display(self.root, handle_open_settings=self.open_settings)

  def open_settings(self):
    settings_window = Tk()
    settings_window.title(settings_ui.SettingsUI.TITLE)
    self.settings.display(settings_window, handle_confirm=lambda config: self.confirm_settings(settings_window, config))

  def confirm_settings(self, window, config):
    self.game.update_settings(config)
    self.display_game()  # Redraw Game Window
    window.destroy()  # Destroy Settings Window


if __name__ == "__main__":
  app = App()
  app.run_game()

