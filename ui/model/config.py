from core.board_layout import BoardLayout
from core.color import Color
from core.player_type import PlayerType
from ui.model.heuristic_type import HeuristicType
from ui.model.agent_type import AgentType


class Config:
    """
    Config defines the customization settings for the program.
    """

    DEFAULT_LAYOUT = BoardLayout.BELGIAN_DAISY
    DEFAULT_MOVE_LIMIT = 40
    DEFAULT_PLAYER_TYPE_P1 = PlayerType.COMPUTER
    DEFAULT_PLAYER_TYPE_P2 = PlayerType.COMPUTER
    DEFAULT_TIME_LIMIT_P1 = 10.0
    DEFAULT_TIME_LIMIT_P2 = 10.0
    DEFAULT_HEURISTIC_TYPE_P1 = HeuristicType.WEIGHTED_NORMALIZED
    DEFAULT_HEURISTIC_TYPE_P2 = HeuristicType.BRANDON
    DEFAULT_AGENT_TYPE_P1 = AgentType.DEFAULT
    DEFAULT_AGENT_TYPE_P2 = AgentType.BRANDON

    def __init__(self, layout: BoardLayout, move_limit: int,
                 player_type_p1: PlayerType, player_type_p2: PlayerType,
                 time_limit_p1: float, time_limit_p2: float,
                 heuristic_type_p1: HeuristicType, heuristic_type_p2: HeuristicType,
                 agent_type_p1: AgentType, agent_type_p2: AgentType):
        self.layout = layout
        self.move_limit = move_limit
        self.player_type_p1 = player_type_p1
        self.player_type_p2 = player_type_p2
        self.time_limit_p1 = time_limit_p1
        self.time_limit_p2 = time_limit_p2
        self.heuristic_type_p1 = heuristic_type_p1
        self.heuristic_type_p2 = heuristic_type_p2
        self.agent_type_p1 = agent_type_p1
        self.agent_type_p2 = agent_type_p2

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

    @classmethod
    def from_default(cls):
        """
        Sets defaults config values for the program.
        :return: None
        """
        return Config(cls.DEFAULT_LAYOUT, cls.DEFAULT_MOVE_LIMIT,
                      cls.DEFAULT_PLAYER_TYPE_P1, cls.DEFAULT_PLAYER_TYPE_P2,
                      cls.DEFAULT_TIME_LIMIT_P1, cls.DEFAULT_TIME_LIMIT_P2,
                      cls.DEFAULT_HEURISTIC_TYPE_P1, cls.DEFAULT_HEURISTIC_TYPE_P2,
                      cls.DEFAULT_AGENT_TYPE_P1, cls.DEFAULT_AGENT_TYPE_P2)
