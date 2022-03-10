from dataclasses import dataclass, field
from core.move import Move
from core.color import Color

@dataclass
class GameHistoryItem:
    time: float
    move: Move
    color: Color

@dataclass
class GameHistory:
    actions: list[GameHistoryItem] = field(default_factory=list)
