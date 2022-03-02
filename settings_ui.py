from tkinter import OptionMenu, StringVar, Entry
from tkinter.ttk import Frame, Label, Button

from config import Config

class SettingsUI:
  """
  This Class is the GUI representation of the settings for the application.
  """
  TITLE = "Settings"

  COL_SIZE = 200
  ROW_SIZE = 40

  def __init__(self):
    self.config = Config.from_default()

  def on_confirm(self, config, callback):
    """
    :param config: config
    :param callback: callback
    :return: none
    """
    self.config = config
    callback(config)

  def display(self, parent, **kwargs):
    """
    Displays the GUI frame onto the container.
    :param parent: the tkinter container
    :param kwargs: dictionary of arguments
    :return: none
    """
    frame = Frame(parent)
    frame.pack()
    self._render(frame, **kwargs)

  def _render(self, parent, **kwargs):
    """
    Renders the settings GUI and defines the setting components.
    :param parent: the tkinter container
    :param kwargs: dictionary of arguments
    :return: none
    """
    self._render_title(parent)

    layout = self._render_dropdown(parent, 1, "Starting Layout", self.config.layout,
                                   "Standard", "German Daisy", "Belgian Daisy")

    game_mode = self._render_dropdown(parent, 2, "Game Mode", self.config.game_mode,
                                      "Human vs. Computer", "Computer vs. Computer", "Human vs. Human")

    player_color = self._render_dropdown(parent, 3, "Player Color", self.config.player_color,
                                         "White", "Black")

    move_limits = self._render_double_input(parent, 4, "Move Limit", self.config.move_limit_p1, self.config.move_limit_p2)
    time_limits = self._render_double_input(parent, 5, "Time Limit", self.config.time_limit_p1, self.config.time_limit_p2)

    Button(parent, text="Confirm", command=lambda: self.on_confirm(Config(
      layout.get(),
      game_mode.get(),
      player_color.get(),
      move_limits[0].get(),
      move_limits[1].get(),
      time_limits[0].get(),
      time_limits[1].get()
    ), kwargs["handle_confirm"])).grid(column=0, row=6, columnspan=2)

    self._render_grid(parent)

  def _render_title(self, parent):
    """
    Renders the title of the settings GUI.
    :param parent: the tkinter container
    :return: none
    """
    Label(parent, text="Settings", font="Helvetica 16 bold").grid(column=0, row=0, columnspan=2)

  def _render_dropdown(self, parent, row, label, default, value, *values):
    """
    Renders and defines a dropdown menu.
    :param parent: the tkinter container
    :param row: a grid row
    :param label: a string
    :param default: default value
    :param value: a string
    :param values: list of strings
    :return: selected
    """
    Label(parent, text=label).grid(column=0, row=row, sticky='e', ipadx=8)
    selected = StringVar(parent)
    selected.set(default)
    OptionMenu(parent, selected, value, *values).grid(column=1, row=row, sticky='w')
    return selected

  def _render_double_input(self, parent, row, label, default1, default2):
    """
    Renders the adjacent text inputs.
    :param parent: the tkinter container
    :param row: a grid row
    :param label: a string
    :param default1: a string
    :param default2: a string
    :return: chosen input
    """
    Label(parent, text=label).grid(column=0, row=row, sticky='e', ipadx=8)
    sub_frame = Frame(parent)
    sub_frame.grid(column=1, row=row, sticky='w')

    input_1 = Entry(sub_frame, width=5)
    input_1.insert(0, default1)
    input_1.grid(column=0, row=0, sticky='w')

    input_2 = Entry(sub_frame, width=5)
    input_2.insert(0, default2)
    input_2.grid(column=1, row=0, sticky='w', padx=8)

    return input_1, input_2

  def _render_grid(self, parent):
    """
    Renders the grid for the settings
    :param parent: a tkinter container
    :return:  none
    """
    col_count, row_count = parent.grid_size()

    for col in range(col_count):
      parent.grid_columnconfigure(col, minsize=self.COL_SIZE)

    for row in range(row_count):
      parent.grid_rowconfigure(row, minsize=self.ROW_SIZE)
