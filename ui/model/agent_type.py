from enum import Enum

from agent.default.agent import DefaultAgent
from agent.brandon.agent import BrandonAgent
from agent.brandon.agent_ponder import BrandonPonderer


class AgentType(Enum):
    DEFAULT = "Default"
    BRANDON = "2-ply negascout"
    BRANDON_PONDERER = "Ponderer"

    def create(self):
        """
        Creates an agent from the given enum.
        """
        return {
            AgentType.DEFAULT: DefaultAgent,
            AgentType.BRANDON: BrandonAgent,
            AgentType.BRANDON_PONDERER: BrandonPonderer,
        }[self]()
