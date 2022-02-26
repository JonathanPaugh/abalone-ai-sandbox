from tkinter import Canvas, Frame, Label, Button, WORD
from tkinter.scrolledtext import ScrolledText

from board_layout import BoardLayout

class GameUI:
  WINDOW_WIDTH = 480
  WINDOW_HEIGHT = 480

  MARBLE_SIZE = 32
  MARBLE_XMARGIN = 4
  MARBLE_YMARGIN = 1

  BOARD_SIZE = 5
  BOARD_MAXCOLS = BOARD_SIZE * 2 - 1
  BOARD_WIDTH = (MARBLE_SIZE + MARBLE_XMARGIN) * BOARD_MAXCOLS - MARBLE_XMARGIN
  BOARD_HEIGHT = (MARBLE_SIZE + MARBLE_YMARGIN) * BOARD_MAXCOLS - MARBLE_YMARGIN

  def __init__(self):
    self.layout = self.generate_standard_layout()
    self.frame = None

  def set_layout(self, layout):
    layout_options = {
      BoardLayout.Standard: self.generate_standard_layout,
      BoardLayout.German: self.generate_german_layout,
      BoardLayout.Belgian: self.generate_belgian_layout
    }

    self.layout = layout_options[layout]()

  def display(self, parent, **kwargs):
    if self.frame is not None:
      self.frame.destroy()
    self.frame = Frame(parent)
    self.frame.pack()
    self._render(self.frame, **kwargs)

  def _render(self, frame, **kwargs):
    frame.columnconfigure(0, weight=8)
    frame.columnconfigure(1, weight=2)
    frame.rowconfigure(0, weight=2)
    frame.rowconfigure(1, weight=4)
    frame.rowconfigure(2, weight=4)
    self._render_buttons(frame, **kwargs).grid(column=0, row=0, columnspan=2)
    self._render_score(frame).grid(column=1, row=1)
    self._render_history(frame).grid(column=1, row=2)
    self._render_board(frame).grid(column=0, row=1, rowspan=2)

  def _render_buttons(self, parent, **kwargs):
    frame = Frame(parent, borderwidth=1, relief="solid", width=1000, background="#42464c")

    frame.columnconfigure(0, weight=1)
    frame.columnconfigure(1, weight=1)
    frame.columnconfigure(2, weight=1)
    frame.columnconfigure(3, weight=1)
    frame.columnconfigure(4, minsize=320)
    frame.columnconfigure(5, weight=1)

    Label(frame, text='00:00\':00\"', borderwidth=1, relief="solid", font=("Arial", 25)).grid(column=0, row=0)
    Button(frame, text='Pause').grid(column=1, row=0)
    Button(frame, text='Reset').grid(column=2, row=0)
    Button(frame, text='Undo').grid(column=3, row=0)
    Button(frame, text='Settings', command=kwargs["open_settings"]).grid(column=5, row=0)

    for widget in frame.winfo_children():
      widget.grid(padx=3, pady=0)

    return frame

  def _render_history(self, parent):
    frame = Frame(parent, background="#42464c", borderwidth=1, relief="solid")

    Label(frame, background="#42464c", foreground="white",
              text="Move History", font=("Arial", 15), ).grid(column=0, row=0)

    # scrolled text
    text_area = ScrolledText(frame,
                             background="#42464c",
                             foreground='white',
                             wrap=WORD,
                             width=20,
                             height=10,
                             font=("Times New Roman", 15))

    text_area.grid(column=0, pady=10, padx=10)

    return frame

  def _render_score(self, parent):
    frame = Frame(parent, background="#42464c", borderwidth=1, relief="solid")
    frame.columnconfigure(0, minsize=72)  # creates empty space
    frame.columnconfigure(1, weight=8)
    frame.columnconfigure(2, weight=8)
    frame.columnconfigure(3, minsize=72)  # creates empty space
    frame.rowconfigure(0, weight=8)
    frame.rowconfigure(1, weight=8)
    frame.rowconfigure(2, weight=8)
    frame.rowconfigure(3, minsize=5)  # creates empty space
    frame.rowconfigure(4, weight=8)
    frame.rowconfigure(5, weight=8)
    frame.rowconfigure(6, weight=8)

    Label(frame, background="#42464c", foreground="white", text='Player1', font=("Arial", 15)).grid(column=1, row=0, columnspan=2)
    Label(frame, background="#42464c", foreground="white", text='Score:', font=("Arial", 12)).grid(column=1, row=1)
    Label(frame, background="#42464c", foreground="white", text='Test', font=("Arial", 12)).grid(column=2, row=1)
    Label(frame, background="#42464c", foreground="white", text='Moves:', font=("Arial", 12)).grid(column=1, row=2)
    Label(frame, background="#42464c", foreground="white", text='Test', font=("Arial", 12)).grid(column=2, row=2)
    Label(frame, background="#42464c", foreground="white", text='Player2', font=("Arial", 15)).grid(column=1, row=4, columnspan=2)
    Label(frame, background="#42464c", foreground="white", text='Score:', font=("Arial", 12)).grid(column=1, row=5)
    Label(frame, background="#42464c", foreground="white", text='Test', font=("Arial", 12)).grid(column=2, row=5)
    Label(frame, background="#42464c", foreground="white", text='Moves:', font=("Arial", 12)).grid(column=1, row=6)
    Label(frame, background="#42464c", foreground="white", text='Test', font=("Arial", 12)).grid(column=2, row=6)

    for widget in frame.winfo_children():
      widget.grid(padx=2, pady=5)

    return frame

  def _render_board(self, parent):
    canvas = Canvas(parent, width=GameUI.WINDOW_WIDTH, height=GameUI.WINDOW_HEIGHT,
                    highlightthickness=0, background="#42464c")

    pos = (GameUI.WINDOW_WIDTH / 2 - GameUI.BOARD_WIDTH / 2,
           GameUI.WINDOW_HEIGHT / 2 - GameUI.BOARD_HEIGHT / 2)

    for row, line in enumerate(self.layout):
      for col, val in enumerate(line):
        x = (col * (GameUI.MARBLE_SIZE + GameUI.MARBLE_XMARGIN)
             + (GameUI.BOARD_MAXCOLS - len(line)) * (GameUI.MARBLE_SIZE + GameUI.MARBLE_XMARGIN) / 2
             + pos[0])
        y = (row * (GameUI.MARBLE_SIZE + GameUI.MARBLE_YMARGIN)
          + pos[1])
        cell_data = self.layout[row][col]
        circle_color = {
          0: "#ccc",
          1: "#c36",
          2: "#36c",
        }[cell_data]
        canvas.create_oval(x, y, x + GameUI.MARBLE_SIZE, y + GameUI.MARBLE_SIZE, fill=circle_color, outline="")

    return canvas

  @staticmethod
  def generate_empty_board(size):
    board = []
    for i in reversed(range(size)):
      board.insert(0, [0] * (size + i))
      if i < size - 1:
        board.append([0] * (size + i))
    return board

  @staticmethod
  def generate_standard_layout():
    return [
      [1, 1, 1, 1, 1],
      [1, 1, 1, 1, 1, 1],
      [0, 0, 1, 1, 1, 0, 0],
      [0, 0, 0, 0, 0, 0, 0, 0],
      [0, 0, 0, 0, 0, 0, 0, 0, 0],
      [0, 0, 0, 0, 0, 0, 0, 0],
      [0, 0, 2, 2, 2, 0, 0],
      [2, 2, 2, 2, 2, 2],
      [2, 2, 2, 2, 2],
    ]

  @staticmethod
  def generate_german_layout():
    return [
      [0, 0, 0, 0, 0],
      [1, 1, 0, 0, 2, 2],
      [1, 1, 1, 0, 2, 2, 2],
      [0, 1, 1, 0, 0, 2, 2, 0],
      [0, 0, 0, 0, 0, 0, 0, 0, 0],
      [0, 2, 2, 0, 0, 1, 1, 0],
      [2, 2, 2, 0, 1, 1, 1],
      [2, 2, 0, 0, 1, 1],
      [0, 0, 0, 0, 0],
    ]

  @staticmethod
  def generate_belgian_layout():
    return [
      [1, 1, 0, 2, 2],
      [1, 1, 1, 2, 2, 2],
      [0, 1, 1, 0, 2, 2, 0],
      [0, 0, 0, 0, 0, 0, 0, 0],
      [0, 0, 0, 0, 0, 0, 0, 0, 0],
      [0, 0, 0, 0, 0, 0, 0, 0],
      [0, 2, 2, 0, 1, 1, 0],
      [2, 2, 2, 1, 1, 1],
      [2, 2, 0, 1, 1],
    ]
