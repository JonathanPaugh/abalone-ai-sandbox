from math import inf
from tkinter import Tk, Canvas

BOARD_SIZE = 5
MARBLE_SIZE = 32
MARBLE_XMARGIN = 4
MARBLE_YMARGIN = 1
WINDOW_WIDTH = 480
WINDOW_HEIGHT = 480
BOARD_MAXCOLS = BOARD_SIZE * 2 - 1
BOARD_WIDTH = (MARBLE_SIZE + MARBLE_XMARGIN) * BOARD_MAXCOLS - MARBLE_XMARGIN
BOARD_HEIGHT = (MARBLE_SIZE + MARBLE_YMARGIN) * BOARD_MAXCOLS - MARBLE_YMARGIN

root = Tk()
canvas = Canvas(root, width=WINDOW_WIDTH, height=WINDOW_HEIGHT, highlightthickness=0)
canvas.pack()

def generate_empty_board(size):
  board = []
  for i in reversed(range(size)):
    board.insert(0, [0] * (size + i))
    if i < size - 1:
      board.append([0] * (size + i))
  return board

def generate_standard_board():
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

def render_board(board, pos):
  for row, line in enumerate(board):
    for col, val in enumerate(line):
      x = (col * (MARBLE_SIZE + MARBLE_XMARGIN)
        + (BOARD_MAXCOLS - len(line)) * (MARBLE_SIZE + MARBLE_XMARGIN) / 2
        + pos[0])
      y = (row * (MARBLE_SIZE + MARBLE_YMARGIN)
        + pos[1])
      cell_data = board[row][col]
      circle_color = {
        0: "#ccc",
        1: "#c36",
        2: "#36c",
      }[cell_data]
      canvas.create_oval(x, y, x + MARBLE_SIZE, y + MARBLE_SIZE, fill=circle_color, outline="")

board = generate_standard_board()
render_board(board, pos=(
  WINDOW_WIDTH / 2 - BOARD_WIDTH / 2,
  WINDOW_HEIGHT / 2 - BOARD_HEIGHT / 2
))

root.title("Abalone")
root.mainloop()
