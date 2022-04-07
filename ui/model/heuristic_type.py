from __future__ import annotations

from enum import Enum
from numbers import Number

from agent.heuristics.heuristic_jonathan import Heuristic
from agent.heuristics.heuristic_brandon import (
    heuristic_offensive as heuristic_brandon_offensive,
    heuristic_defensive as heuristic_brandon_defensive,
)

from core.board import Board
from core.color import Color


class HeuristicType(Enum):
    WEIGHTED_NORMALIZED = "Weighted Normalized"
    WEIGHTED = "Weighted"
    DYNAMIC = "Dynamic"
    BRANDON_OFFENSIVE = "Offensive Brandon"
    BRANDON_DEFENSIVE = "Defensive Brandon"

    def call(self, board: Board, player: Color) -> Number:
        return {
            HeuristicType.WEIGHTED_NORMALIZED: lambda: Heuristic.weighted_normalized(board, player),
            HeuristicType.WEIGHTED: lambda: Heuristic.weighted(board, player),
            HeuristicType.DYNAMIC: lambda: Heuristic.dynamic(board, player),
            HeuristicType.BRANDON_OFFENSIVE: lambda: heuristic_brandon_offensive(board, player),
            HeuristicType.BRANDON_DEFENSIVE: lambda: heuristic_brandon_defensive(board, player),
        }[self]()
