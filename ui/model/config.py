from dataclasses import dataclass
from core.board_layout import BoardLayout
from core.color import Color
from core.player_type import PlayerType
from ui.model.heuristic_type import HeuristicType
from ui.model.agent_type import AgentType


@dataclass
class Config:
    """
    Config defines the customization settings for the program.
    """

    layout: BoardLayout = BoardLayout.BELGIAN_DAISY
    move_limit: int = 40
    player_type_p1: PlayerType = PlayerType.HUMAN
    player_type_p2: PlayerType = PlayerType.COMPUTER
    time_limit_p1: float = 10.0
    time_limit_p2: float = 10.0
    heuristic_type_p1: HeuristicType = HeuristicType.BRANDON_OFFENSIVE
    heuristic_type_p2: HeuristicType = HeuristicType.BRANDON_DEFENSIVE
    agent_type_p1: AgentType = AgentType.BRANDON_PONDERER
    agent_type_p2: AgentType = AgentType.BRANDON

    @classmethod
    def from_default(cls):
        """
        Sets defaults config values for the program.
        :return: None
        """
        return Config()

    def get_player_type(self, color: Color):
        return {
            Color.BLACK: self.player_type_p1,
            Color.WHITE: self.player_type_p2
        }[color]

    def get_player_time_limit(self, color: Color):
        return {
            Color.BLACK: self.time_limit_p1,
            Color.WHITE: self.time_limit_p2
        }[color]

    def get_player_heuristic_type(self, color: Color):
        return {
            Color.BLACK: self.heuristic_type_p1,
            Color.WHITE: self.heuristic_type_p2
        }[color]

    def get_player_agent_type(self, color: Color):
        return {
            Color.BLACK: self.agent_type_p1,
            Color.WHITE: self.agent_type_p2
        }[color]
