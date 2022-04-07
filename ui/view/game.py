
"""
Defines the game view.
"""
import tkinter
from tkinter import Frame, Label, Button, Canvas, WORD, StringVar
from tkinter.scrolledtext import ScrolledText
from datetime import timedelta

from core.color import Color
import ui.constants as constants
from ui.view.board import BoardView
import ui.view.colors.palette as palette
from ui.view.colors.transform import lighten_color, darken_color
from ui.view.colors.themes import ThemeLibrary
from ui.view.marble import render_marble


class GameUI:
    """
    The view for the game window.
    """

    COLOR_FOREGROUND_PRIMARY = "#FFFFFF"
    COLOR_BACKGROUND_PRIMARY = palette.COLOR_GRAY_200
    COLOR_BACKGROUND_SECONDARY = palette.COLOR_GRAY_400

    FONT_FAMILY_PRIMARY = "Arial"
    FONT_FAMILY_SECONDARY = "Arial"

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

    PLAYER_COLOR_MAP = {
        "Player 1": Color.BLACK,
        "Player 2": Color.WHITE
    }

    TURN_CANVAS_SIZE = 16
    TURN_ICON_SIZE = TURN_CANVAS_SIZE - 2

    def __init__(self):
        self.frame = None
        self._board_view = None
        self._timer_text = None
        self._score_1 = None
        self._score_2 = None
        self._move_count_1 = None
        self._move_count_2 = None
        self._paused = None
        self._theme = constants.DEFAULT_THEME
        self._history_1 = ""
        self._history_2 = ""
        self._cached_turn_indicators = {}
        self._cached_score_headings = {}


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

        self._paused.set("Resume" if model.paused else "Pause")

        self._score_1.set(str(model.game_board.get_score(Color.BLACK)))
        self._score_2.set(str(model.game_board.get_score(Color.WHITE)))
        self._move_count_1.set(str(model.get_turn_count(Color.BLACK)))
        self._move_count_2.set(str(model.get_turn_count(Color.WHITE)))
        self._history_1.delete(1.0, tkinter.END)
        self._history_2.delete(1.0, tkinter.END)
        self._history_1.insert(tkinter.INSERT, model.history.get_player_history_string(Color.BLACK))
        self._history_2.insert(tkinter.INSERT, model.history.get_player_history_string(Color.WHITE))

        self._update_turn_indicators(model)

    def _find_color_by_marble(self, marble):
        color = lighten_color(self._theme.get_color_by_key(marble))

        # lighten black again for readability
        # TODO: un-hardcode this
        if self._theme is ThemeLibrary.MONOCHROME:
            color = lighten_color(color)

        return color

    def _mount_widgets(self, parent,
                       on_click_undo=None, on_click_pause=None, on_click_stop=None,
                       on_click_reset=None, on_click_settings=None, on_click_board=None):
        """
        Renders all components required for the GUI.
        :param parent: the tkinter container
        :param kwargs: dictionary of arguments
        :return: None
        """

        self._mount_buttonbar(parent, on_click_undo, on_click_pause, on_click_stop, on_click_reset, on_click_settings)

        self._mount_score_player1(parent, "Player 1",
            colour=self._find_color_by_marble(Color.BLACK),
            row=1, column=1)
        self._mount_score_player2(parent, "Player 2",
            colour=self._find_color_by_marble(Color.WHITE),
            row=2, column=2)

        self._mount_history_1(parent)
        self._mount_history_2(parent)
        self._mount_board(self.frame, on_click=on_click_board)
        self._configure_grid(parent)

    def _mount_history_1(self, parent):
        """
        Renders the match history for player 1 for the GUI portion.
        :param parent: the tkinter container
        :return:
        """
        frame = Frame(parent, background=self.COLOR_BACKGROUND_SECONDARY, borderwidth=1, relief="solid")
        frame.grid(column=1, row=2)
        self._history_1 = ScrolledText(frame,
                                 background=self.COLOR_BACKGROUND_SECONDARY,
                                 foreground=self.COLOR_FOREGROUND_PRIMARY,
                                 insertbackground=self.COLOR_FOREGROUND_PRIMARY,
                                 wrap=WORD,
                                 width=15,
                                 height=15,
                                 font=self.FONT_HISTORY
                                 )
        self._history_1.grid(column=0, pady=(20, 20), padx=10)

    def _mount_history_2(self, parent):
        """
        Renders the match history for player 2 for the GUI portion.
        :param parent: the tkinter container
        :return:
        """
        frame = Frame(parent, background=self.COLOR_BACKGROUND_SECONDARY, borderwidth=1, relief="solid")
        frame.grid(column=2, row=2)
        self._history_2 = ScrolledText(frame,
                                 background=self.COLOR_BACKGROUND_SECONDARY,
                                 foreground=self.COLOR_FOREGROUND_PRIMARY,
                                 insertbackground=self.COLOR_FOREGROUND_PRIMARY,
                                 wrap=WORD,
                                 width=15,
                                 height=15,
                                 font=self.FONT_HISTORY
                                 )
        self._history_2.grid(column=0, pady=(20, 20), padx=10)

    def _mount_buttonbar(self, parent, on_click_undo, on_click_pause, on_click_stop, on_click_reset, on_click_settings):
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
        frame.columnconfigure(4, weight=1)
        frame.columnconfigure(5, minsize=460)
        frame.columnconfigure(6, weight=1)

        self._timer_text = StringVar(frame, "00:00.00")
        Label(frame,
              textvariable=self._timer_text,
              font=(self.FONT_FAMILY_PRIMARY, 25),
              foreground=self.COLOR_FOREGROUND_PRIMARY,
              background=self.COLOR_BACKGROUND_SECONDARY).grid(column=0, row=0)

        self._paused = StringVar(frame, "Pause")

        self._mount_buttonbar_button(frame, 1, "Undo", command=on_click_undo)
        self._mount_buttonbar_button(frame, 2, "", textvariable=self._paused, command=on_click_pause)
        self._mount_buttonbar_button(frame, 3, "Stop", command=on_click_stop)
        self._mount_buttonbar_button(frame, 4, "Reset", command=on_click_reset)
        self._mount_buttonbar_button(frame, 6, "Settings", command=on_click_settings)

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

    def _mount_score_player1(self, parent, player, colour, row, column):
        """
        Renders a score board.
        :param parent: the tkinter container
        :return: a frame
        """
        self._score_1 = StringVar(parent, "0")
        self._move_count_1 = StringVar(parent, "0")
        frame = self._mount_score_board(parent, colour, player, row, column)
        self._score_1 = StringVar(parent, "0")
        self._move_count_1 = StringVar(parent, "0")
        Label(frame, background=self.COLOR_BACKGROUND_SECONDARY, foreground=self.COLOR_FOREGROUND_PRIMARY,
              textvariable=self._score_1,
              font=self.FONT_MEDIUM).grid(column=2, row=row + 1)
        Label(frame, background=self.COLOR_BACKGROUND_SECONDARY, foreground=self.COLOR_FOREGROUND_PRIMARY,
              textvariable=self._move_count_1,
              font=self.FONT_MEDIUM).grid(column=2, row=row + 2)

        return frame

    def _mount_score_player2(self, parent, player, colour, row, column):
        """
        Renders a score board.
        :param parent: the tkinter container
        :return: a frame
        """
        self._score_2 = StringVar(parent, "0")
        self._move_count_2 = StringVar(parent, "0")
        frame = self._mount_score_board(parent, colour, player, row, column)
        self._score_2 = StringVar(parent, "0")
        self._move_count_2 = StringVar(parent, "0")
        Label(frame, background=self.COLOR_BACKGROUND_SECONDARY, foreground=self.COLOR_FOREGROUND_PRIMARY,
              textvariable=self._score_2,
              font=self.FONT_MEDIUM).grid(column=2, row=row + 1)
        Label(frame, background=self.COLOR_BACKGROUND_SECONDARY, foreground=self.COLOR_FOREGROUND_PRIMARY,
              textvariable=self._move_count_2,
              font=self.FONT_MEDIUM).grid(column=2, row=row + 2)
        return frame

    def _mount_score_board(self, parent, colour, player, row, column):
        """
        Defines and renders the text for displaying static items for score and move.
        """

        frame_score = Frame(parent, background=self.COLOR_BACKGROUND_SECONDARY, borderwidth=1, relief="solid")
        frame_score.grid(column=column, row=1, padx=5, pady=5)
        Label(frame_score, background=self.COLOR_BACKGROUND_SECONDARY, foreground=self.COLOR_FOREGROUND_PRIMARY,
              text="Score:", font=self.FONT_MEDIUM).grid(column=1, row=row + 1)
        Label(frame_score, background=self.COLOR_BACKGROUND_SECONDARY, foreground=self.COLOR_FOREGROUND_PRIMARY,
              text="Moves:", font=self.FONT_MEDIUM).grid(column=1, row=row + 2)
        self._mount_score_grid(frame_score)

        frame_heading = Frame(frame_score, background=self.COLOR_BACKGROUND_SECONDARY)
        frame_heading.grid(column=1, row=row, columnspan=2)

        turn_icon_canvas = Canvas(frame_heading,
            width=self.TURN_CANVAS_SIZE, height=self.TURN_CANVAS_SIZE,
            background=self.COLOR_BACKGROUND_SECONDARY,
            highlightthickness=0)
        render_marble(
            turn_icon_canvas,
            pos=(self.TURN_CANVAS_SIZE / 2, self.TURN_CANVAS_SIZE / 2),
            color=darken_color(colour),
            size=self.TURN_ICON_SIZE,
            selected=True,
        )
        turn_icon_canvas.pack(side="left")

        player_color = self.PLAYER_COLOR_MAP[player]
        self._cached_turn_indicators[player_color] = turn_icon_canvas

        score_heading = self._mount_score_heading(frame_heading, player, colour)
        score_heading.pack(side="left", padx=2)
        self._cached_score_headings[player_color] = score_heading

        return frame_score

    def _mount_score_heading(self, parent, label, colour):
        """
        :param parent: the tkinter container
        :param row: a grid row
        :param label: a string
        :return: none
        """
        return Label(parent, background=self.COLOR_BACKGROUND_SECONDARY, foreground=colour,
                     text=label, font=self.FONT_LARGE)

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

    def _update_turn_indicators(self, model):
        for color, canvas in self._cached_turn_indicators.items():
            canvas.delete("all")
            marble_color = self._theme.get_color_by_key(color)
            is_marble_player_turn = (model.game_turn == color)
            render_marble(
                canvas,
                pos=(self.TURN_CANVAS_SIZE / 2, self.TURN_CANVAS_SIZE / 2),
                color=marble_color,
                size=self.TURN_ICON_SIZE,
                selected=not is_marble_player_turn,
            )

    def apply_move(self, *args, **kwargs):
        """
        Visually moves the marbles affected by the given move.
        :param *args, **kwargs: the action parameters
        :return: None
        """
        self._board_view.apply_move(*args, **kwargs)

    def apply_config(self, config):
        self._theme = config.theme
        self._board_view.apply_config(config)

        self._cached_score_headings[Color.BLACK].config(
            foreground=self._find_color_by_marble(Color.BLACK))

        self._cached_score_headings[Color.WHITE].config(
            foreground=self._find_color_by_marble(Color.WHITE))
