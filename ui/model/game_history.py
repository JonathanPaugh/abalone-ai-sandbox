"""
Generic interface for game history.
"""

from dataclasses import dataclass, field
from typing import List

from core.move import Move
from core.color import Color


@dataclass
class GameHistoryItem:
    """
    A game history item.
    """

    time_start: float
    time_end: float
    move: Move
    color: Color # TODO(?): color can be inferred by stack position - remove?

@dataclass
class GameHistory:
    """
    A simple interface around the game history stack.

    Game history unlocks a non-negligible chunk of the application's core
    functionality:
    - The current game turn may be deduced via Color.next(history[-1].color)
    - The current game ply may be deduced via floor(len(history))
    - The time taken for a move is the delta of `time_start` and `time_end`
    - Total aggregate time for a given player may be determined via the
    summation of all `time_end` - `time_start` deltas
    - "Time-travel" undo logic may be achieved by reconstructing the game board
    using all moves within history[:-1] starting from the starting layout
    (i.e. the more space-efficient implementation)
    """

    actions: List[GameHistoryItem] = field(default_factory=list)

    def __getitem__(self, index):
        """
        Gets the item at the specified index.
        :param index: an int
        :return: a HistoryItem
        """

    def __len__(self):
        """
        Determines the length of the history stack.
        :return: an int
        """

    def append(self, item):
        """
        Appends an item to the history stack.
        :param item: a HistoryItem
        :return: None
        """

    def pop(self):
        """
        Pops an item off the history stack.
        :return: a HistoryItem
        """
