from __future__ import annotations
from enum import Enum, auto
from dataclasses import dataclass
from core.move import Move


@dataclass
class TranspositionTable:

    class EntryType(Enum):
        PV = auto()
        CUT = auto()
        ALL = auto()

    @dataclass
    class Entry:
        score: float = None
        depth: int = None
        move: Move = None
        type: TranspositionTable.EntryType = None
