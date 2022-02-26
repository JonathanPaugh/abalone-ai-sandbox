from tkinter import Frame

import game_ui
from board_layout import BoardLayout

class Game:
  TITLE = "Abalone"

  def __init__(self):
    self.game_ui = game_ui.GameUI()
    self.window = None

  def display(self, parent, **kwargs):
    self.game_ui.display(parent, **kwargs)

  def update_settings(self, config):
    # Set up game with settings here from config param
    layout = BoardLayout.from_string(config.layout)
    self.game_ui.set_layout(layout)