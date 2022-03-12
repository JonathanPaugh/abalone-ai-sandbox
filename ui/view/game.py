"""
Defines the game view.
"""

from tkinter import Frame, Label, Button, WORD
from tkinter.scrolledtext import ScrolledText

import ui.constants as constants
from ui.view.board import BoardView


class GameUI:
    """
    The view for the game window.
    """

    COLOR_FOREGROUND_PRIMARY = "#FFFFFF"
    COLOR_BACKGROUND_PRIMARY = "#36393E"
    COLOR_BACKGROUND_SECONDARY = "#42464C"

    FONT_FAMILY_PRIMARY = "Arial"
    FONT_FAMILY_SECONDARY = "Times New Roman"

    FONT_LARGE = FONT_FAMILY_PRIMARY, 15
    FONT_MEDIUM = FONT_FAMILY_PRIMARY, 12
    FONT_HISTORY = FONT_FAMILY_SECONDARY, 15

    WINDOW_PADDING = 16

    BOARD_CELL_SIZE = constants.BOARD_CELL_SIZE
    MARBLE_SIZE = constants.MARBLE_SIZE
    BOARD_SIZE = constants.BOARD_SIZE
    BOARD_MAX_COLS = constants.BOARD_MAX_COLS
    BOARD_WIDTH = BOARD_CELL_SIZE * BOARD_MAX_COLS
    BOARD_HEIGHT = BOARD_CELL_SIZE * BOARD_MAX_COLS * 7 / 8

    def __init__(self):
        self.frame = None
        self._board_view = None

    def mount(self, parent, **kwargs):
        """
        Displays the GUI.
        :param parent: the tkinter container
        :param kwargs: dictionary of arguments
        :return: None
        """
        if self.frame is not None:
            self.frame.destroy()
        self.frame = Frame(parent, background=self.COLOR_BACKGROUND_PRIMARY, padx=self.WINDOW_PADDING,
                           pady=self.WINDOW_PADDING)
        self.frame.pack(fill="both")
        self._mount_widgets(self.frame, **kwargs)

    def render(self, model):
        """
        Diffs the given model against game view state and queues up changes to
        display on update.
        :param model: the model to render
        :return: None
        """
        self._board_view.render(model)

    def _mount_widgets(self, parent, on_click_settings, on_click_board):
        """
        Renders all components required for the GUI.
        :param parent: the tkinter container
        :param kwargs: dictionary of arguments
        :return: None
        """
        self._mount_buttonbar(parent, on_click_settings)
        self._mount_score(parent)
        self._mount_history(parent)
        self._mount_board(self.frame, on_click=on_click_board)
        self._configure_grid(parent)

    def _mount_buttonbar(self, parent, on_click_settings):
        """
        Renders the button bar.
        :param parent: the tkinter container
        :param kwargs: dictionary of arguments
        :return: a frame
        """
        frame = Frame(parent, borderwidth=1, relief="solid", background=self.COLOR_BACKGROUND_SECONDARY)
        frame.grid(column=0, row=0, columnspan=2)

        frame.columnconfigure(0, weight=1)
        frame.columnconfigure(1, weight=1)
        frame.columnconfigure(2, weight=1)
        frame.columnconfigure(3, weight=1)
        frame.columnconfigure(4, minsize=320)
        frame.columnconfigure(5, weight=1)
        frame.columnconfigure(6, weight=1)

        Label(frame,
              text="00:00.00",
              font=(self.FONT_FAMILY_PRIMARY, 25),
              foreground=self.COLOR_FOREGROUND_PRIMARY,
              background=self.COLOR_BACKGROUND_SECONDARY
        ).grid(column=0, row=0)

        self._mount_buttonbar_button(frame, 1, "Pause")
        self._mount_buttonbar_button(frame, 2, "Reset")
        self._mount_buttonbar_button(frame, 3, "Undo")
        self._mount_buttonbar_button(frame, 5, "Settings", command=on_click_settings)
        self._mount_buttonbar_button(frame, 6, "Stop")

        for widget in frame.winfo_children():
            widget.grid(padx=3, pady=0)

        return frame

    def _mount_buttonbar_button(self, parent, col, label, **kwargs):
        """

        :param parent: the tkinter container
        :param col: grid column
        :param label: a string
        :param kwargs: dictionary of arguments
        :return: None
        """
        Button(parent, text=label, fg=self.COLOR_FOREGROUND_PRIMARY,
               bg=self.COLOR_BACKGROUND_SECONDARY, **kwargs).grid(column=col, row=0)

    def _mount_score(self, parent):
        """
        Renders a score board.
        :param parent: the tkinter container
        :return: a frame
        """
        frame = Frame(parent, background=self.COLOR_BACKGROUND_SECONDARY, borderwidth=1, relief="solid")
        frame.grid(column=1, row=1)

        self._mount_score_heading(frame, 0, "Player 1")
        self._mount_score_field(frame, 1, "Score", "Test")
        self._mount_score_field(frame, 2, "Moves", "Test")
        self._mount_score_heading(frame, 4, "Player 2")
        self._mount_score_field(frame, 5, "Score", "Test")
        self._mount_score_field(frame, 6, "Moves", "Test")

        self._mount_score_grid(frame)

        for widget in frame.winfo_children():
            widget.grid(padx=2, pady=5)

        return frame

    def _mount_score_heading(self, parent, row, label):
        """

        :param parent: the tkinter container
        :param row: a grid row
        :param label: a string
        :return: none
        """
        Label(parent, background=self.COLOR_BACKGROUND_SECONDARY, foreground=self.COLOR_FOREGROUND_PRIMARY, text=label,
              font=self.FONT_LARGE).grid(column=1, row=row, columnspan=2)

    def _mount_score_field(self, parent, row, label, value):
        """
        :param parent: the tkinter container
        :param row: a grid row
        :param label: a string
        :param value: an int
        :return: none
        """
        Label(parent, background=self.COLOR_BACKGROUND_SECONDARY, foreground=self.COLOR_FOREGROUND_PRIMARY,
              text=F"{label}:", font=self.FONT_MEDIUM).grid(column=1, row=row)
        Label(parent, background=self.COLOR_BACKGROUND_SECONDARY, foreground=self.COLOR_FOREGROUND_PRIMARY, text=value,
              font=self.FONT_MEDIUM).grid(column=2, row=row)

    def _mount_score_grid(self, parent):
        """
        Defines and renders the grid for displaying score.
        Renders the score grid with
        :param parent: the tkinter container
        :return: none
        """
        parent.columnconfigure(0, minsize=72)  # creates empty space
        parent.columnconfigure(1, weight=8)
        parent.columnconfigure(2, weight=8)
        parent.columnconfigure(3, minsize=72)  # creates empty space
        parent.rowconfigure(0, weight=8)
        parent.rowconfigure(1, weight=8)
        parent.rowconfigure(2, weight=8)
        parent.rowconfigure(3, minsize=5)  # creates empty space
        parent.rowconfigure(4, weight=8)
        parent.rowconfigure(5, weight=8)
        parent.rowconfigure(6, weight=8)

    def _mount_history(self, parent):
        """
        Renders the match history GUI portion.
        :param parent: the tkinter container
        :return:
        """
        frame = Frame(parent, background=self.COLOR_BACKGROUND_SECONDARY, borderwidth=1, relief="solid")
        frame.grid(column=1, row=2)

        Label(frame, background=self.COLOR_BACKGROUND_SECONDARY, foreground=self.COLOR_FOREGROUND_PRIMARY,
              text="Move History", font=self.FONT_LARGE).grid(column=0, row=0)

        text_area = ScrolledText(frame,
                                 background=self.COLOR_BACKGROUND_SECONDARY,
                                 foreground=self.COLOR_FOREGROUND_PRIMARY,
                                 insertbackground=self.COLOR_FOREGROUND_PRIMARY,
                                 wrap=WORD,
                                 width=20,
                                 height=10,
                                 font=self.FONT_HISTORY)

        text_area.grid(column=0, pady=10, padx=10)

        return frame

    def _mount_board(self, parent, on_click):
        """
        Renders the layout board.
        :param parent: the tkinter container
        :return: canvas
        """
        board_view = BoardView()
        self._board_view = board_view

        canvas = board_view.mount(parent, on_click)
        canvas.configure(background=self.COLOR_BACKGROUND_SECONDARY)
        canvas.grid(column=0, row=1, rowspan=2)
        return canvas

    def _configure_grid(self, parent):
        """
        Defines and renders the main grid of the GUI.
        :param parent: the tkinter container
        :return: none
        """
        parent.columnconfigure(0, weight=8)
        parent.columnconfigure(1, weight=2)
        parent.rowconfigure(0, weight=2)
        parent.rowconfigure(1, weight=4)
        parent.rowconfigure(2, weight=4)

    def apply_move(self, *args, **kwargs):
        """
        Visually moves the marbles affected by the given move.
        :param *args, **kwargs: the action parameters
        :return: None
        """
        self._board_view.apply_move(*args, **kwargs)
