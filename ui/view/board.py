"""
Defines the board view.
"""

from math import sqrt
from abc import ABC, abstractmethod
from tkinter import Canvas
from lib.compose_fns import compose_fns
from lib.easing_expo import ease_out, ease_in
from lib.hex.transpose_hex import hex_to_point, point_to_hex
from lib.anims.tween import TweenAnim

from core.hex import Hex
from core.color import Color

import ui.view.colors.palette as palette
from ui.view.colors.themes import ThemeKey
from ui.view.anims.hex_tween import HexTweenAnim
from ui.view.marble import Marble, render_marble
from ui.constants import (
    BOARD_SIZE, BOARD_MAX_COLS,
    BOARD_CELL_SIZE, MARBLE_SIZE,
    BOARD_WIDTH, BOARD_HEIGHT,
    DEFAULT_THEME,
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


class MarbleAnim(ABC):
    """
    A generic marble animation.
    Defines the `transform` method for composing marble drawing parameters.
    For more complex operands, consider wrapping drawing parameters into their
    own class.
    """

    @abstractmethod
    def transform(self, cell, size):
        """
        Transforms the given marble drawing parameters using the animation state.
        :param cell: a Hex
        :param size: a float
        :return: a tuple[Hex, float]
        """

class MarbleMoveAnim(MarbleAnim, HexTweenAnim):
    """
    A marble movement animation.
    Usage requires a `src` and `dest` per `HexTweenAnim`.
    """
    duration = 10

    def transform(self, _, size):
        """
        Transforms the given marble drawing parameters using the animation state.
        :param cell: a Hex
        :param size: a float
        :return: a tuple[Hex, float]
        """
        return self.cell, size

class MarbleShrinkAnim(MarbleAnim, TweenAnim):
    """
    A marble shrink animation.
    """
    duration = 7

    def transform(self, cell, size):
        """
        Transforms the given marble drawing parameters using the animation state.
        :param cell: a Hex
        :param size: a float
        :return: a tuple[Hex, float]
        """
        return cell, size * (1 - self.pos)


class BoardView:
    """
    The board view.
    Displays a hexagonal board populated with marbles.
    """

    PADDING = 8
    COLOR_PLAYER_NONE = palette.COLOR_GRAY_700

    def __init__(self):
        self._canvas = None
        self._theme = DEFAULT_THEME
        self._marbles = []
        self._anims = []

    @property
    def animating(self):
        """
        Determines whether or not the board is being animated.
        :return: a bool
        """
        # TODO: performance bottleneck - use update flag or animation class
        return next((True for anim in self._anims if not anim.done), False)

    def _setup(self, model):
        """
        Performs the initial board render.
        :param model: the Model to render based on
        :return: a Canvas
        """

        canvas = self._canvas

        marble_items = []
        for cell, color in model.game_board.enumerate():
            pos = self._find_marble_pos(cell)
            self._render_cell(canvas, pos)
            if color:
                marble_items.append((pos, cell, color))

        for pos, cell, color in marble_items:
            self._marbles.append(Marble(
                pos=pos,
                cell=cell,
                color=color,
                object_ids=render_marble(
                    canvas,
                    pos=pos,
                    color=self._theme.get_color_by_key(color),
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

    def _refresh(self, model):
        """
        Updates the board using the given model.
        :param model: the Model to diff against
        :return: None
        """
        for marble in self._marbles:
            self._refresh_marble(model, marble)

    def _refresh_marble(self, model, marble):
        """
        Refreshes a marble using the given model.
        :param model: the Model to diff against
        :param marble: the Marble to clear
        :return: None
        """

        # redraw marble if state has changed
        is_marble_selected = model.selection and marble.cell in model.selection.to_array()
        is_marble_focused = (model.selection
            and marble.cell == (model.selection.end or model.selection.start))
        is_marble_highlighted = (model.history
            and marble.cell in model.history[-1].move.get_destinations())

        if (is_marble_selected != marble.selected
        or is_marble_focused != marble.focused
        or is_marble_highlighted != marble.highlighted):
            marble.selected = is_marble_selected
            marble.focused = is_marble_focused
            marble.highlighted = is_marble_highlighted
            self._redraw_marble(marble,
                selected=is_marble_selected,
                focused=is_marble_focused,
                highlighted=is_marble_highlighted)

    def _update_marble(self, marble, anims):
        marble_cell = marble.cell
        marble_size = MARBLE_SIZE

        for anim in anims:
            marble_cell, marble_size = anim.transform(marble_cell, marble_size)

        new_pos = self._find_marble_pos(marble_cell)
        old_x, old_y = marble.pos
        new_x, new_y = new_pos
        marble.pos = new_pos

        delta = (new_x - old_x, new_y - old_y)
        if delta != (0, 0):
            for object_id in marble.object_ids:
                self._canvas.move(object_id, *delta)

        if marble_size != MARBLE_SIZE:
            for object_id in marble.object_ids:
                marble_scale = marble_size / MARBLE_SIZE
                self._canvas.scale(object_id, *new_pos, marble_scale, marble_scale)

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

        if marble in self._marbles:
            self._marbles.remove(marble)

    def _redraw_marble(self, marble, selected=False, focused=False, highlighted=False):
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
            color=self._theme.get_color_by_key(marble.color),
            size=MARBLE_SIZE,
            selected=selected,
            focused=focused,
            highlighted=highlighted,
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

    def _update_anims(self):
        """
        Updates the board's animations by one tick.
        :return: None
        """
        self._anims = [anim for anim in self._anims if not anim.done]
        for anim in self._anims:
            if not anim.done:
                anim.update()

    def _update_marbles(self):
        """
        Updates the board's marbles by one tick.
        :return: None
        """
        if not self._anims:
            return

        for marble in self._marbles:
            marble_anims = [anim for anim in self._anims if anim.target is marble]
            if marble_anims:
                self._update_marble(marble, anims=marble_anims)

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

    def update(self):
        """
        Updates the game board view by a single tick.
        :return: None
        """
        self._update_anims()
        self._update_marbles()

    def render(self, model):
        """
        Diffs the given model against view state and queues up changes to
        display on update.
        Uses cached marbles if existent; draws new ones otherwise
        :param model: the model to render
        :return: None
        """
        if self._marbles:
            self._refresh(model)
        else:
            self._setup(model)

    def clear(self):
        """
        Clears the entire game board.
        :return: None
        """
        self._canvas.delete("all")
        self._marbles.clear()

    def apply_move(self, move, board, on_end=None):
        """
        Visually moves the marbles affected by the given move.
        :param move: the Move to apply
        :param board: the Board to apply the move onto (for sumito detection)
        :return: None
        """

        move_color = move.get_player(board)
        move_cells = move.get_cells()
        move_target = move.get_front_target()

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
            self._anims.append(MarbleMoveAnim(
                target=marble,
                easing=ease_out,
                src=cell,
                dest=marble.cell,
            ))

            if marble.cell not in board:
                self._anims.append(MarbleShrinkAnim(
                    target=marble,
                    easing=ease_in,
                    delay=MarbleMoveAnim.duration,
                    on_end=(lambda marble: (
                        lambda: self._delete_marble(marble)
                    ))(marble)
                ))

        if self._anims:
            self._anims[-1].on_end = compose_fns(self._anims[-1].on_end, on_end)

    def apply_config(self, config):
        self._theme = config.theme
        print("set theme to", self._theme)
