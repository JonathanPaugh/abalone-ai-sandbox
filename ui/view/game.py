"""
Defines the game view.
"""

from tkinter import Frame, Label, Button, WORD, StringVar
from tkinter.scrolledtext import ScrolledText
from datetime import timedelta

import ui.constants as constants
from core.color import Color
from ui.view.board import BoardView


class GameUI:
    """
    The view for the game window.
    """

    COLOR_FOREGROUND_PRIMARY = "#FFFFFF"
    COLOR_BACKGROUND_PRIMARY = "#36393E"
    COLOR_BACKGROUND_SECONDARY = "#42464C"
    COLOR_PLAYER_RED = "#e64343"
    COLOR_PLAYER_BLUE = "#4343e6"

    FONT_FAMILY_PRIMARY = "Arial"
    FONT_FAMILY_SECONDARY = "Times New Roman"

    FONT_LARGE = FONT_FAMILY_PRIMARY, 18
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
        self._timer_text = None
        self._score_1 = None
        self._score_2 = None
        self._move_count_1 = None
        self._move_count_2 = None

    @property
    def animating(self):
        """
        Determines whether or not the game is being animated.
        :return: a bool
        """
        return self._board_view.animating

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

        self._score_1.set(str(model.game_board.get_score(Color.WHITE)))
        self._score_2.set(str(model.game_board.get_score(Color.BLACK)))
        self._move_count_1.set(str(model.game.temporary_move_count[0]))
        self._move_count_2.set(str(model.game.temporary_move_count[1]))

    def _mount_widgets(self, parent, on_click_settings, on_click_board):
        """
        Renders all components required for the GUI.
        :param parent: the tkinter container
        :param kwargs: dictionary of arguments
        :return: None
        """

        self._mount_buttonbar(parent, on_click_settings)
        self._mount_score_player1(parent, "Player 1", self.COLOR_PLAYER_BLUE, 1)
        self._mount_score_player2(parent, "Player 2", self.COLOR_PLAYER_RED, 2)
        self._mount_history(parent, 1)
        self._mount_history(parent, 2)
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
        frame.grid(column=0, row=0, columnspan=5, padx=(20, 0))

        frame.columnconfigure(0, weight=1)
        frame.columnconfigure(1, weight=1)
        frame.columnconfigure(2, weight=1)
        frame.columnconfigure(3, weight=1)
        frame.columnconfigure(4, minsize=460)
        frame.columnconfigure(5, weight=1)
        frame.columnconfigure(6, weight=1)

        self._timer_text = StringVar(frame, "00:00.00")
        Label(frame,
              textvariable=self._timer_text,
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
            widget.grid(padx=4, pady=0)

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

    def _mount_score_player1(self, parent, player, colour, row):
        """
        Renders a score board.
        :param parent: the tkinter container
        :return: a frame
        """
        frame = Frame(parent, background=self.COLOR_BACKGROUND_SECONDARY, borderwidth=1, relief="solid")
        frame.grid(column=1, row=1, padx=5, pady=5)

        self._score_1 = StringVar(parent, "0")
        self._move_count_1 = StringVar(parent, "0")

        self._mount_score_heading(frame, 0, player, colour)
        Label(frame, background=self.COLOR_BACKGROUND_SECONDARY, foreground=self.COLOR_FOREGROUND_PRIMARY,
              text="Scores:", font=self.FONT_MEDIUM).grid(column=1, row=row)
        Label(frame, background=self.COLOR_BACKGROUND_SECONDARY, foreground=self.COLOR_FOREGROUND_PRIMARY,
              textvariable=self._score_1,
              font=self.FONT_MEDIUM).grid(column=2, row=row)
        Label(frame, background=self.COLOR_BACKGROUND_SECONDARY, foreground=self.COLOR_FOREGROUND_PRIMARY,
              text="Moves:", font=self.FONT_MEDIUM).grid(column=1, row=row + 1)
        Label(frame, background=self.COLOR_BACKGROUND_SECONDARY, foreground=self.COLOR_FOREGROUND_PRIMARY,
              textvariable=self._move_count_1,
              font=self.FONT_MEDIUM).grid(column=2, row=row + 1)

        self._mount_score_grid(frame)

        for widget in frame.winfo_children():
            widget.grid(padx=2, pady=(0, 10))

        return frame

    def _mount_score_player2(self, parent, player, colour, row):
        """
        Renders a score board.
        :param parent: the tkinter container
        :return: a frame
        """
        frame = Frame(parent, background=self.COLOR_BACKGROUND_SECONDARY, borderwidth=1, relief="solid")
        frame.grid(column=2, row=1, padx=5, pady=5)

        self._score_2 = StringVar(parent, "0")
        self._move_count_2 = StringVar(parent, "0")

        self._mount_score_heading(frame, 0, player, colour)
        Label(frame, background=self.COLOR_BACKGROUND_SECONDARY, foreground=self.COLOR_FOREGROUND_PRIMARY,
              text="Score:", font=self.FONT_MEDIUM).grid(column=1, row=row)
        Label(frame, background=self.COLOR_BACKGROUND_SECONDARY, foreground=self.COLOR_FOREGROUND_PRIMARY,
              textvariable=self._score_2,
              font=self.FONT_MEDIUM).grid(column=2, row=row)
        Label(frame, background=self.COLOR_BACKGROUND_SECONDARY, foreground=self.COLOR_FOREGROUND_PRIMARY,
              text="Moves:", font=self.FONT_MEDIUM).grid(column=1, row=row + 1)
        Label(frame, background=self.COLOR_BACKGROUND_SECONDARY, foreground=self.COLOR_FOREGROUND_PRIMARY,
              textvariable=self._move_count_2,
              font=self.FONT_MEDIUM).grid(column=2, row=row + 1)

        self._mount_score_grid(frame)

        for widget in frame.winfo_children():
            widget.grid(padx=2, pady=(0, 10))

        return frame

    def _mount_score_heading(self, parent, row, label, colour):
        """

        :param parent: the tkinter container
        :param row: a grid row
        :param label: a string
        :return: none
        """
        Label(parent, background=self.COLOR_BACKGROUND_SECONDARY, foreground=colour, text=label,
              font=self.FONT_LARGE).grid(column=1, row=row, columnspan=2)

    def _mount_score_grid(self, parent):
        """
        Defines and renders the grid for displaying score.
        Renders the score grid with
        :param parent: the tkinter container
        :return: none
        """
        parent.columnconfigure(0, minsize=45)  # creates empty space
        parent.columnconfigure(1, weight=8)
        parent.columnconfigure(2, weight=8)
        parent.columnconfigure(3, minsize=45)  # creates empty space

    def _mount_history(self, parent, area):
        """
        Renders the match history GUI portion.
        :param parent: the tkinter container
        :return:
        """
        frame = Frame(parent, background=self.COLOR_BACKGROUND_SECONDARY, borderwidth=1, relief="solid")
        frame.grid(column=area, row=2)

        text_area = ScrolledText(frame,
                                 background=self.COLOR_BACKGROUND_SECONDARY,
                                 foreground=self.COLOR_FOREGROUND_PRIMARY,
                                 insertbackground=self.COLOR_FOREGROUND_PRIMARY,
                                 wrap=WORD,
                                 width=15,
                                 height=15,
                                 font=self.FONT_HISTORY,
                                 state='disabled'
                                 )

        text_area.grid(column=0, pady=(20, 20), padx=10)

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
        canvas.grid(column=0, row=1, rowspan=2, padx=20, pady=10)
        return canvas

    def _configure_grid(self, parent):
        """
        Defines and renders the main grid of the GUI.
        :param parent: the tkinter container
        :return: none
        """
        parent.columnconfigure(0, weight=10)
        parent.columnconfigure(1, weight=1)
        parent.columnconfigure(2, weight=1)
        parent.rowconfigure(0, weight=2)
        parent.rowconfigure(1, weight=4)
        parent.rowconfigure(2, weight=4)

    def clear_board(self):
        """
        Clears the entire game board.
        :return: None
        """
        self._board_view.clear()

    def update(self):
        """
        Updates the game view by one tick.
        """
        self._board_view.update()

    def update_timer(self, time: timedelta):
        """
        Updates the game view timer.
        :param time: a time to display.
        """
        time_string = str(time)
        minutes, seconds = time_string.split(":")[1:]
        seconds_string = F"{int(float(seconds))}".zfill(2)
        milliseconds_string = F"{int(time.microseconds / pow(10, 3))}".zfill(3)
        self._timer_text.set(F"{minutes}:{seconds_string}.{milliseconds_string}")

    def apply_move(self, *args, **kwargs):
        """
        Visually moves the marbles affected by the given move.
        :param *args, **kwargs: the action parameters
        :return: None
        """
        self._board_view.apply_move(*args, **kwargs)
