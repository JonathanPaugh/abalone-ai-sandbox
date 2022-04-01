from tkinter import Toplevel, OptionMenu, StringVar, Entry, CENTER
from tkinter.ttk import Frame, Label, Button

from agent.heuristics.heuristic_type import HeuristicType
from core.player_type import PlayerType
from ui.model.config import Config
from core.board_layout import BoardLayout


class SettingsUI:
    """
    This Class is the GUI representation of the settings for the application.
    """
    FONT_FAMILY_HEADING = "Helvetica"

    FONT_TITLE = FONT_FAMILY_HEADING, 18, "bold"
    FONT_HEADING = FONT_FAMILY_HEADING, 14, "bold"

    TITLE = "Settings"

    COL_SIZE = 60
    ROW_SIZE = 40

    STARTING_LAYOUT_MAP = {
        "Standard": BoardLayout.STANDARD,
        "German Daisy": BoardLayout.GERMAN_DAISY,
        "Belgian Daisy": BoardLayout.BELGIAN_DAISY,
    }

    def __init__(self, config, on_close):
        self.config = config or Config.from_default()
        self._window = None
        self._on_close = on_close
        self._destroyed = False

    def open(self):
        """
        Opens the settings window.
        :return: None
        """
        window = Toplevel()
        frame = Frame(window)
        frame.pack()
        self._window = window
        window.protocol("WM_DELETE_WINDOW", self.cancel)
        self._mount(frame)
        return self

    def destroy(self):
        if self._destroyed:
            return

        self._destroyed = True
        self._window.destroy()

    def cancel(self):
        if self._destroyed:
            return

        self._on_close(None)
        self.destroy()

    def _mount(self, parent):
        """
        Renders the settings GUI and defines the setting components.
        :param parent: the tkinter container
        :param kwargs: dictionary of arguments
        :return: none
        """
        self._mount_title(parent, 0)

        starting_layout = [*self.STARTING_LAYOUT_MAP.keys()][0]
        layout = self._mount_starting_layout(parent, 1, starting_layout)

        move_limit = self._mount_move_limit(parent, 2)

        self._mount_player_labels(parent, 3)

        player_type_p1, player_type_p2 = self._mount_player_types(parent, 4)

        time_limit_p1, time_limit_p2 = self._mount_time_limits(parent, 5)

        heuristic_type_p1, heuristic_type_p2 = self._mount_heuristic_types(parent, 6)

        Button(parent, text="Confirm", command=lambda: (
            self._on_close(Config(
                next((v for k, v in self.STARTING_LAYOUT_MAP.items() if layout.get() == k), starting_layout),
                int(move_limit.get()),
                PlayerType(player_type_p1.get()),
                PlayerType(player_type_p2.get()),
                float(time_limit_p1.get()),
                float(time_limit_p2.get()),
                HeuristicType(heuristic_type_p1.get()),
                HeuristicType(heuristic_type_p2.get()),
            )),
            self.destroy(),
        )).grid(column=0, row=7, columnspan=5)

        self._configure_grid(parent)

    def _mount_title(self, parent, row):
        """
        Renders the title of the settings GUI.
        :param parent: the tkinter container
        :return: none
        """
        Label(parent, text="Settings", font=self.FONT_TITLE).grid(column=0, row=row, columnspan=5)

    def _mount_starting_layout(self, parent, row, default):
        self._mount_label(parent, row, 1, "e", "Starting Layout")
        return self._mount_dropdown(parent, row, 3, "w",
                                     next((k for k, v in self.STARTING_LAYOUT_MAP.items() if v == self.config.layout),
                                     default), *self.STARTING_LAYOUT_MAP.keys())

    def _mount_player_labels(self, parent, row):
        Label(parent, text="Blue Player", font=self.FONT_HEADING, justify=CENTER).grid(column=1, row=row, pady=(8, 4))
        Label(parent, text="Red Player", font=self.FONT_HEADING, justify=CENTER).grid(column=3, row=row, pady=(8, 4))

    def _mount_move_limit(self, parent, row):
        self._mount_label(parent, row, 1, "e", "Move Limit")
        return self._mount_input(parent, row, 3, "w", self.config.move_limit)

    def _mount_player_types(self, parent, row):
        options = [player_type.value for player_type in PlayerType]
        p1 = self._mount_dropdown(parent, row, 1, "e", self.config.player_type_p1.value, *options)
        self._mount_label(parent, row, 2, "", "Player Type")
        p2 = self._mount_dropdown(parent, row, 3, "w", self.config.player_type_p2.value, *options)
        return p1, p2

    def _mount_time_limits(self, parent, row):
        p1 = self._mount_input(parent, row, 1, "e", self.config.time_limit_p1)
        self._mount_label(parent, row, 2, "", "Time Limit")
        p2 = self._mount_input(parent, row, 3, "w", self.config.time_limit_p2)
        return p1, p2

    def _mount_heuristic_types(self, parent, row):
        options = [heuristic_type.value for heuristic_type in HeuristicType]
        p1 = self._mount_dropdown(parent, row, 1, "e", self.config.heuristic_type_p1.value, *options)
        self._mount_label(parent, row, 2, "", "Heuristic Type")
        p2 = self._mount_dropdown(parent, row, 3, "w", self.config.heuristic_type_p2.value, *options)
        return p1, p2

    def _mount_label(self, parent, row, col, anchor, label):
        Label(parent, text=label).grid(column=col, row=row, sticky=anchor, padx=8)

    def _mount_dropdown(self, parent, row, col, anchor, default, value, *values):
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
        selected = StringVar(parent)
        selected.set(default)
        OptionMenu(parent, selected, value, *values).grid(column=col, row=row, sticky=anchor)
        return selected

    def _mount_input(self, parent, row, col, anchor, default):
        """
        Renders the adjacent text inputs.
        :param parent: the tkinter container
        :param row: a grid row
        :param label: a string
        :param default1: a string
        :param default2: a string
        :return: chosen input
        """
        sub_frame = Frame(parent)
        sub_frame.grid(column=col, row=row, sticky=anchor)

        input = Entry(sub_frame, width=5)
        input.insert(0, default)
        input.grid(column=0, row=0, sticky=anchor)

        return input

    def _configure_grid(self, parent):
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
