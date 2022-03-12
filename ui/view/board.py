"""
Defines the board view.
"""

from math import sqrt
from tkinter import Canvas
from lib.hex.transpose_hex import hex_to_point, point_to_hex

from core.hex import Hex
from core.color import Color

import ui.view.colors.palette as palette
from ui.view.marble import Marble, render_marble
from ui.constants import (
    BOARD_SIZE, BOARD_MAX_COLS,
    BOARD_CELL_SIZE, MARBLE_SIZE,
    BOARD_WIDTH, BOARD_HEIGHT
)


HEX_XRADIUS = BOARD_CELL_SIZE / 2
HEX_YRADIUS = BOARD_CELL_SIZE / sqrt(3)

def point_to_hex_with_board_offsets(pos):
    """
    Converts the given point to a hex coordinate, taking into account board
    offsets.
    Provides an adapter for `point_to_hex`, which performs the point to hex
    conversion relative to the origin (0, 0).
    :param pos: a tuple[int, int]
    :return: a Hex
    """
    x, y = pos
    x += -(BOARD_MAX_COLS - BOARD_SIZE + 1) * HEX_XRADIUS
    y += -HEX_XRADIUS
    cell = point_to_hex((x, y), HEX_YRADIUS)
    return Hex(cell[0] + BOARD_MAX_COLS // 2, cell[1])


class BoardView:
    """
    The board view.
    Displays a hexagonal board populated with marbles.
    """

    PADDING = 8
    COLOR_PLAYER_NONE = "#48535A"
    MARBLE_COLORS = {
        Color.BLACK: palette.COLOR_BLUE,
        Color.WHITE: palette.COLOR_RED,
    }

    def __init__(self):
        self._canvas = None
        self._marbles = []

    def _setup(self, model):
        """
        Performs the initial board render.
        :param model: the Model to render based on
        :return: a Canvas
        """

        canvas = self._canvas

        marble_items = []
        for cell, color in model.game_board.enumerate(): # TODO(?): demeter
            pos = self._find_marble_pos(cell)
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

    def _find_marble_pos(self, cell):
        """
        Finds the true position on the board associated with the given cell.
        Used to render marbles and board cells.
        :param cell: the Hex to find the position for
        :return: a tuple[int, int]
        """
        x, y = hex_to_point((cell.x, cell.y), BOARD_CELL_SIZE / 2)
        return (x + self.PADDING, y + self.PADDING)

    def _find_marble_by_cell(self, cell):
        """
        Finds the marble associated with the given cell.
        :param cell: the Hex to check for Marble instances in
        :return: a Marble if existent, else None
        """
        return next((marble for marble in self._marbles if marble.cell == cell), None)

    def _update(self, model):
        """
        Updates the board using the given model.
        :param model: the Model to diff against
        :return: None
        """
        for marble in self._marbles:
            self._update_marble(model, marble)

    def _update_marble(self, model, marble):
        """
        Updates a marble using the given model.
        :param model: the Model to diff against
        :param marble: the Marble to clear
        :return: None
        """

        # redraw marble if state has changed
        is_marble_selected = model.selection and marble.cell in model.selection.to_array()
        is_marble_focused = (model.selection
            and marble.cell == (model.selection.end or model.selection.start))
        if (is_marble_selected != marble.selected
        or is_marble_focused != marble.focused):
            marble.selected = is_marble_selected
            marble.focused = is_marble_focused
            self._redraw_marble(marble, selected=is_marble_selected, focused=is_marble_focused)

        # adjust marble positions based on cell changes
        marble_pos = self._find_marble_pos(marble.cell)
        for object_id in marble.object_ids:
            old_x, old_y = marble.pos
            new_x, new_y = marble_pos
            delta = (new_x - old_x, new_y - old_y)
            if delta != (0, 0):
                self._canvas.move(object_id, *delta)

        marble.pos = marble_pos

    def _clear_marble(self, marble):
        """
        Clears a marble's objects from the board.
        :param marble: the Marble to clear
        :return: None
        """
        for object_id in marble.object_ids:
            self._canvas.delete(object_id)

    def _delete_marble(self, marble):
        """
        Permanently deletes a marble from the board.
        :param marble: the Marble to delete
        :return: None
        """
        self._clear_marble(marble)
        self._marbles.remove(marble)

    def _redraw_marble(self, marble, selected=False, focused=False):
        """
        Destroys and redraws a marble.
        Used for redrawing different marble states.
        :param marble: the Marble to redraw
        :param selected: a bool denoting whether or not the marble is selected
        :param focused: a bool denoting whether or not the marble is focused
        :return: None
        """
        self._clear_marble(marble)
        marble.object_ids = render_marble(
            self._canvas,
            pos=marble.pos,
            color=self.MARBLE_COLORS[marble.color],
            size=MARBLE_SIZE,
            selected=selected,
            focused=focused,
        )

    def _render_cell(self, canvas, pos):
        """
        Renders a cell (i.e. marble slot).
        :param canvas: the Canvas to render onto
        :param pos: the position to render the cell to
        :return: None
        """
        x, y = pos
        canvas.create_oval(
            x - MARBLE_SIZE / 2, y - MARBLE_SIZE / 2,
            x + MARBLE_SIZE / 2, y + MARBLE_SIZE / 2,
            fill=BoardView.COLOR_PLAYER_NONE,
            outline="",
        )

    def mount(self, parent, on_click):
        """
        Mounts the board view onto the given parent.
        :param parent: the Widget to mount the board view onto
        :param on_click: a func[tuple[int, int]] that handles click events
        """
        canvas = Canvas(parent,
            width=BOARD_WIDTH + self.PADDING * 2,
            height=BOARD_HEIGHT + self.PADDING * 2,
            highlightthickness=0)
        canvas.bind("<Button-1>", lambda event: (
            pos := (event.x - self.PADDING, event.y - self.PADDING),
            cell := point_to_hex_with_board_offsets(pos),
            on_click(cell),
        ))
        self._canvas = canvas
        return canvas

    def render(self, model):
        """
        Diffs the given model against view state and queues up changes to
        display on update.
        Uses cached marbles if existent; draws new ones otherwise
        :param model: the model to render
        :return: None
        """
        if self._marbles:
            self._update(model)
        else:
            self._setup(model)

    def apply_move(self, move, board):
        """
        Visually moves the marbles affected by the given move.
        :param move: the Move to apply
        :param board: the Board to apply the move onto (for sumito detection)
        :return: None
        """

        move_color = move.selection.get_player(board) # TODO: demeter
        move_cells = move.selection.to_array() # TODO: demeter
        move_head = move.get_front()

        # TODO: add method for getting move target cell
        move_target = move_head and move_head.add(move.direction.value)

        # perform a sumito if target cell contains one of the opponent's marbles
        if move_target and board[move_target] == Color.next(move_color):
            sumito_selection = board.select_marbles_in_line(
                start=move_target,
                direction=move.direction
            )
            # add cells to list of cells to move
            move_cells += sumito_selection.to_array() if sumito_selection else []

        marble_cells = [(marble, cell) for cell in move_cells
            if (marble := self._find_marble_by_cell(cell))]

        for marble, cell in marble_cells:
            marble.cell = cell.add(move.direction.value)
            if marble.cell not in board:
                self._delete_marble(marble)
