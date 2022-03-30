"""
Generic interface for game history.
"""

from dataclasses import dataclass
import time


class GameHistoryItem:
    """
    A game history item.
    """

    # time_start: float
    # time_end: float
    # move: Move
    # color: Color # TODO(?): color can be inferred by stack position - remove?

    def __init__(self, time_start, move):
        self.time_start = time_start
        # self.time_end= time_end
        self.move = move
        # self._color: color


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

    def __init__(self):
        self._history = [GameHistoryItem(time.time(), None), GameHistoryItem(time.time(), None)]

    def __getitem__(self, index):
        """
        Gets the item at the specified index.
        :param index: an int
        :return: a HistoryItem
        """
        return self._history[index]

    def __len__(self):
        """
        Determines the length of the history stack.
        :return: an int
        """
        return len(self._history)

    def append(self, item):
        """
        Appends an item to the history stack.
        :param item: a HistoryItem
        :return: None
        """
        self._history.append(item)

    def pop(self):
        """
        Pops an item off the history stack.
        :return: a HistoryItem
        """
        return self._history.pop()

    def get_player_1_history(self):
        """
        Gets a string of player 1 history.
        :return: a String
        """
        history_string = ""
        player_1_history = self._history[0::2]
        for i in range(1, len(player_1_history)):
            history_string += \
                str(i) + "." + "\n" + \
                self.get_player_1_total_time(i-1) + " >>> " + \
                self.get_player_1_total_time(i) + "\n" + \
                str(player_1_history[i].move) + "\n"
        return history_string

    def get_player_2_history(self):
        """
        Gets a string of player 2 history.
        :return: a String
        """
        history_string = ""
        player_2_history = self._history[1::2]
        for i in range(1, len(player_2_history)):
            history_string += \
                str(i)+"." + "\n" +\
                self.get_player_2_total_time(i-1) + " >>> " + \
                self.get_player_2_total_time(i) + "\n" + \
                str(player_2_history[i].move) + "\n"
        return history_string

    def get_player_1_total_time(self, past_move):
        """
        Gets the total time for player 1.
        """
        player_1_history = self._history[0::2]
        player_2_history = self._history[1::2]
        total_time = 0
        for i in range(1, past_move + 1):
            total_time += player_1_history[i].time_start - player_2_history[i - 1].time_start
        return format(total_time, '.2f')

    def get_player_2_total_time(self, past_move):
        """
        Gets the total time for player 2.
        """
        player_1_history = self._history[0::2]
        player_2_history = self._history[1::2]
        total_time = 0
        for i in range(1, past_move+1):
            total_time += player_2_history[i].time_start - player_1_history[i].time_start
        return format(total_time, '.2f')
