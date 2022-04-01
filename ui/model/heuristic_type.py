from __future__ import annotations

from enum import Enum
from numbers import Number

from agent.heuristics.heuristic_jonathan import Heuristic
from agent.heuristics.heuristic_brandon import heuristic as heuristic_brandon

from core.board import Board
from core.color import Color


class HeuristicType(Enum):
    WEIGHTED_NORMALIZED = "Weighted Normalized"
    WEIGHTED = "Weighted"
    DYNAMIC = "Dynamic"
    BRANDON = "Brandon"

    def call(self, board: Board, player: Color) -> Number:
        return {
            HeuristicType.WEIGHTED_NORMALIZED: lambda: Heuristic.weighted_normalized(board, player),
            HeuristicType.WEIGHTED: lambda: Heuristic.weighted(board, player),
            HeuristicType.DYNAMIC: lambda: Heuristic.dynamic(board, player),
            HeuristicType.BRANDON: lambda: heuristic_brandon(board, player)
        }[self]()
