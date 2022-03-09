from tkinter import Frame, Canvas, Label, Button, WORD
from tkinter.scrolledtext import ScrolledText

from core.color import Color
from core import constants


class GameUI:
    """
    This class creates the GUI using tkinter and contains methods to create and render the layout.
    """
    COLOR_FOREGROUND_PRIMARY = "#FFFFFF"
    COLOR_BACKGROUND_PRIMARY = "#36393E"
    COLOR_BACKGROUND_SECONDARY = "#42464C"

    COLOR_PLAYER_NONE = "#48535A"
    COLOR_PLAYER_1 = "#3366CC"
    COLOR_PLAYER_2 = "#CC3366"

    FONT_FAMILY_PRIMARY = "Arial"
    FONT_FAMILY_SECONDARY = "Times New Roman"

    FONT_LARGE = FONT_FAMILY_PRIMARY, 15
    FONT_MEDIUM = FONT_FAMILY_PRIMARY, 12
    FONT_HISTORY = FONT_FAMILY_SECONDARY, 15

    WINDOW_PADDING = 16

    MAIN_WIDTH = 480
    MAIN_HEIGHT = 480

    MARBLE_SIZE = 32
    MARBLE_MARGIN_X = 4
    MARBLE_MARGIN_Y = 1

    BOARD_SIZE = constants.BOARD_SIZE
    BOARD_MAX_COLS = constants.BOARD_MAX_COLS
    BOARD_WIDTH = (MARBLE_SIZE + MARBLE_MARGIN_X) * BOARD_MAX_COLS - MARBLE_MARGIN_X
    BOARD_HEIGHT = (MARBLE_SIZE + MARBLE_MARGIN_Y) * BOARD_MAX_COLS - MARBLE_MARGIN_Y

    def __init__(self):
        self.frame = None

    def display(self, parent, board, **kwargs):
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
        self._render(self.frame, board, **kwargs)

    def _render(self, parent, board, **kwargs):
        """
        Renders all components required for the GUI.
        :param parent: the tkinter container
        :param kwargs: dictionary of arguments
        :return: None
        """
        self._render_buttonbar(parent, **kwargs)
        self._render_score(parent)
        self._render_history(parent)
        self._render_board(parent, board)
        self._configure_grid(parent)

    def _render_buttonbar(self, parent, **kwargs):
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

        Label(frame, text="00':00\".00", font=(self.FONT_FAMILY_PRIMARY, 25),
              foreground=self.COLOR_FOREGROUND_PRIMARY, background=self.COLOR_BACKGROUND_SECONDARY).grid(column=0,
                                                                                                         row=0)
        self._render_buttonbar_button(frame, 1, "Pause")
        self._render_buttonbar_button(frame, 2, "Reset")
        self._render_buttonbar_button(frame, 3, "Undo")
        self._render_buttonbar_button(frame, 5, "Settings", command=kwargs["handle_open_settings"])
        self._render_buttonbar_button(frame, 6, "Stop")

        for widget in frame.winfo_children():
            widget.grid(padx=3, pady=0)

        return frame

    def _render_buttonbar_button(self, parent, col, label, **kwargs):
        """

        :param parent: the tkinter container
        :param col: grid column
        :param label: a string
        :param kwargs: dictionary of arguments
        :return: None
        """
        Button(parent, text=label, fg=self.COLOR_FOREGROUND_PRIMARY,
               bg=self.COLOR_BACKGROUND_SECONDARY, **kwargs).grid(column=col, row=0)

    def _render_score(self, parent):
        """
        Renders a score board.
        :param parent: the tkinter container
        :return: a frame
        """
        frame = Frame(parent, background=self.COLOR_BACKGROUND_SECONDARY, borderwidth=1, relief="solid")
        frame.grid(column=1, row=1)

        self._render_score_heading(frame, 0, "Player 1")
        self._render_score_field(frame, 1, "Score", "Test")
        self._render_score_field(frame, 2, "Moves", "Test")
        self._render_score_heading(frame, 4, "Player 2")
        self._render_score_field(frame, 5, "Score", "Test")
        self._render_score_field(frame, 6, "Moves", "Test")

        self._render_score_grid(frame)

        for widget in frame.winfo_children():
            widget.grid(padx=2, pady=5)

        return frame

    def _render_score_heading(self, parent, row, label):
        """

        :param parent: the tkinter container
        :param row: a grid row
        :param label: a string
        :return: none
        """
        Label(parent, background=self.COLOR_BACKGROUND_SECONDARY, foreground=self.COLOR_FOREGROUND_PRIMARY, text=label,
              font=self.FONT_LARGE).grid(column=1, row=row, columnspan=2)

    def _render_score_field(self, parent, row, label, value):
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

    def _render_score_grid(self, parent):
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

    def _render_history(self, parent):
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

    def _render_board(self, parent, board):
        """
        Renders the layout board.
        :param parent: the tkinter container
        :return: canvas
        """
        canvas = Canvas(parent, width=self.MAIN_WIDTH, height=self.MAIN_HEIGHT,
                        highlightthickness=0, background=self.COLOR_BACKGROUND_SECONDARY)
        canvas.grid(column=0, row=1, rowspan=2)

        pos = (self.MAIN_WIDTH / 2 - self.BOARD_WIDTH / 2,
               self.MAIN_HEIGHT / 2 - self.BOARD_HEIGHT / 2)

        for cell, color in board.enumerate():
            q, r = cell.x, cell.y
            x = (q * (self.MARBLE_SIZE + self.MARBLE_MARGIN_X)
                 + (self.BOARD_MAX_COLS - board.width(r) - board.offset(r) * 2)
                 * (self.MARBLE_SIZE + self.MARBLE_MARGIN_X) / 2
                 + pos[0])
            y = (r * (self.MARBLE_SIZE + self.MARBLE_MARGIN_Y)
                 + pos[1])
            circle_color = {
                None: self.COLOR_PLAYER_NONE,
                Color.BLACK: self.COLOR_PLAYER_1,
                Color.WHITE: self.COLOR_PLAYER_2,
            }[color]
            canvas.create_oval(x, y, x + self.MARBLE_SIZE, y + self.MARBLE_SIZE, fill=circle_color, outline="")

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

    @staticmethod
    def generate_empty_board(size):
        """
        Generates an empty board.
        :param size: an int
        :return: a board
        """
        board = []
        for i in reversed(range(size)):
            board.insert(0, [0] * (size + i))
            if i < size - 1:
                board.append([0] * (size + i))
        return board
