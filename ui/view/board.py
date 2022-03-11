from tkinter import Canvas
from lib.hex.transpose_hex import hex_to_point

from core.color import Color
from core.constants import BOARD_CELL_SIZE, MARBLE_SIZE, BOARD_WIDTH, BOARD_HEIGHT

import ui.view.colors.palette as palette
from ui.view.marble import render_marble


class BoardView:

    COLOR_PLAYER_NONE = "#48535A"

    def __init__(self):
        self._canvas = None

    def setup(self, parent, on_click):
        canvas = Canvas(parent, width=BOARD_WIDTH, height=BOARD_HEIGHT, highlightthickness=0)
        canvas.bind("<Button-1>", lambda event: on_click((event.x, event.y)))
        self._canvas = canvas
        return canvas

    def render(self, board):
        canvas = self._canvas

        MARBLE_COLORS = {
            Color.BLACK: palette.COLOR_BLUE,
            Color.WHITE: palette.COLOR_RED,
        }

        for cell, color in board.enumerate():
            q, r = cell.x, cell.y
            x, y = hex_to_point((q, r), BOARD_CELL_SIZE / 2)

            canvas.create_oval(x, y, x + MARBLE_SIZE, y + MARBLE_SIZE, fill=BoardView.COLOR_PLAYER_NONE, outline="")
            if color not in MARBLE_COLORS:
                continue

            render_marble(canvas,
                pos=(x + MARBLE_SIZE / 2, y + MARBLE_SIZE / 2),
                color=MARBLE_COLORS[color],
                size=MARBLE_SIZE)

        return canvas
