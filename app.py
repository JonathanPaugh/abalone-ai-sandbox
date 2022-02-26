import game
import settings_ui
from tkinter import Tk

class App:
  DIMENSIONS = "800x600"

  def __init__(self):
    self.root = Tk()
    self.game = game.Game()
    self.settings = settings_ui.SettingsUI()

  def run_game(self):
    self.display_game()
    self.root.title(game.Game.TITLE)
    self.root.geometry(App.DIMENSIONS)
    self.root.attributes('-toolwindow', True)
    self.root.configure(background="#36393E")
    self.root.mainloop()

  def display_game(self):
    self.game.display(self.root, open_settings=self.open_settings)

  def open_settings(self):
    settings_window = Tk()
    self.settings.display(settings_window, confirm_settings=lambda config: self.confirm_settings(settings_window, config))
    settings_window.title(settings_ui.SettingsUI.TITLE)

  def confirm_settings(self, window, config):
    self.game.update_settings(config)
    self.display_game()
    window.destroy()


if __name__ == "__main__":
  app = App()
  app.run_game()

