from abc import abstractmethod
from enum import Enum, auto
from core.board import Board
from core.color import Color
from agent.base import BaseAgent


class PonderingAgent(BaseAgent):
    """
    A base class for agents with pondering capabilities.
    """

    class SearchMode(Enum):
        """
        Enumerates possible search modes.
        """
        NORMAL_SEARCH = auto()
        PONDER_SEARCH = auto()

    @abstractmethod
    def ponder(self, board: Board, player: Color,
              on_find: callable, on_complete: callable = None):
        """
        Start the search using a board and a player as a starting state.
        :param on_find: A function that gets called everytime a better move is found.
        :param on_complete: A function that gets called when a search runs to exhaustion without
        interruption.
        """
