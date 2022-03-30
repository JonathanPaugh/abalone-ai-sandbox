from __future__ import annotations

from enum import Enum
from numbers import Number

from agent.heuristics.heuristic import Heuristic
from core.board import Board
from core.color import Color


class HeuristicType(Enum):
    WEIGHTED_NORMALIZED = "Weighted Normalized"
    WEIGHTED = "Weighted"
    DYNAMIC = "Dynamic"

    def call(self, board: Board, player: Color) -> Number:
        return {
            HeuristicType.WEIGHTED_NORMALIZED: lambda: Heuristic.weighted_normalized(board, player),
            HeuristicType.WEIGHTED: lambda: Heuristic.weighted(board, player),
            HeuristicType.DYNAMIC: lambda: Heuristic.dynamic(board, player)
        }[self]()
