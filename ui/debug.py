from enum import Enum, auto


class DebugType(Enum):
    Base = auto()
    Warning = auto()
    Game = auto()
    Agent = auto()


class Debug:
    # Turn to false if you want to turn off logging for something
    ACTIVE_DEBUG_TYPES = {
        DebugType.Base: True,
        DebugType.Warning: True,
        DebugType.Game: True,
        DebugType.Agent: True,
    }

    @classmethod
    def log(cls, message: str, debug_type: DebugType = DebugType.Base):
        if cls.ACTIVE_DEBUG_TYPES[debug_type]:
            print(message)
