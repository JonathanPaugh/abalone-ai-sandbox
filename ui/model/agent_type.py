from enum import Enum

from agent.default import Agent as DefaultAgent
from agent.brandon import BrandonAgent


class AgentType(Enum):
    DEFAULT = "Default"
    BRANDON = "2-ply negamax"

    def create(self):
        """
        Creates an agent from the given enum.
        """
        return {
            AgentType.DEFAULT: DefaultAgent,
            AgentType.BRANDON: BrandonAgent,
        }[self]()
