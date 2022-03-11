from dataclasses import dataclass
from tkinter import Canvas
from lib.hex.transpose_hex import hex_to_point

from core.color import Color
from core.constants import BOARD_CELL_SIZE, MARBLE_SIZE, BOARD_WIDTH, BOARD_HEIGHT

import ui.view.colors.palette as palette
from ui.view.marble import render_marble


@dataclass
class Marble:
    pos: tuple[float]
    cell: tuple[int]
    color: Color
    object_ids: list
    selected: bool = False
    focused: bool = False

class BoardView:

    COLOR_PLAYER_NONE = "#48535A"
    MARBLE_COLORS = {
        Color.BLACK: palette.COLOR_BLUE,
        Color.WHITE: palette.COLOR_RED,
    }

    def __init__(self):
        self._canvas = None
        self._marbles = []

    def mount(self, parent, on_click):
        canvas = Canvas(parent, width=BOARD_WIDTH, height=BOARD_HEIGHT, highlightthickness=0)
        canvas.bind("<Button-1>", lambda event: on_click((event.x, event.y)))
        self._canvas = canvas
        return canvas

    def _setup(self, model):
        canvas = self._canvas

        marble_items = []
        for cell, color in model.game_board.enumerate():
            pos = hex_to_point((cell.x, cell.y), BOARD_CELL_SIZE / 2)
            self._render_cell(canvas, pos)
            if not self._marbles and color:
                marble_items.append((pos, cell, color))

        for pos, cell, color in marble_items:
            self._marbles.append(Marble(
                pos=pos,
                cell=cell,
                color=color,
                object_ids=render_marble(
                    canvas,
                    pos=pos,
                    color=BoardView.MARBLE_COLORS[color],
                    size=MARBLE_SIZE,
                )
            ))

        return canvas

    def _render_cell(self, canvas, pos):
        x, y = pos
        canvas.create_oval(
            x - MARBLE_SIZE / 2, y - MARBLE_SIZE / 2,
            x + MARBLE_SIZE / 2, y + MARBLE_SIZE / 2,
            fill=BoardView.COLOR_PLAYER_NONE,
            outline="",
        )

    def _redraw(self, model):
        for marble in self._marbles:
            self._update_marble(model, marble)

    def _update_marble(self, model, marble):
        is_marble_selected = model.selection and marble.cell in model.selection.to_array()
        is_marble_focused = model.selection and marble.cell == (model.selection.end or model.selection.start)
        if (is_marble_selected, is_marble_focused) != (marble.selected, marble.focused):
            marble.selected = is_marble_selected
            marble.focused = is_marble_focused
            self._redraw_marble(marble, selected=is_marble_selected, focused=is_marble_focused)

    def _redraw_marble(self, marble, selected=False, focused=False):
        for object_id in marble.object_ids:
            self._canvas.delete(object_id)

        marble.object_ids = render_marble(
            self._canvas,
            pos=marble.pos,
            color=BoardView.MARBLE_COLORS[marble.color],
            size=MARBLE_SIZE,
            selected=selected,
            focused=focused,
        )

    def render(self, board):
        if self._marbles:
            self._redraw(board)
        else:
            self._setup(board)

    def update(self):
        pass
