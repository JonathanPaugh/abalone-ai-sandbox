from agent.heuristics.heuristic_type import HeuristicType
from core.board_layout import BoardLayout
from core.color import Color
from core.player_type import PlayerType


class Config:
    """
    Config defines the customization settings for the program.
    """

    DEFAULT_LAYOUT = BoardLayout.GERMAN_DAISY
    DEFAULT_MOVE_LIMIT = 50
    DEFAULT_PLAYER_TYPE_P1 = PlayerType.COMPUTER
    DEFAULT_PLAYER_TYPE_P2 = PlayerType.COMPUTER
    DEFAULT_TIME_LIMIT_P1 = 60.0
    DEFAULT_TIME_LIMIT_P2 = 60.0
    DEFAULT_HEURISTIC_TYPE_P1 = HeuristicType.DYNAMIC
    DEFAULT_HEURISTIC_TYPE_P2 = HeuristicType.WEIGHTED_NORMALIZED

    def __init__(self, layout: BoardLayout, move_limit: int,
                 player_type_p1: PlayerType, player_type_p2: PlayerType,
                 time_limit_p1: float, time_limit_p2: float,
                 heuristic_type_p1: HeuristicType, heuristic_type_p2: HeuristicType):
        self.layout = layout
        self.move_limit = move_limit
        self.player_type_p1 = player_type_p1
        self.player_type_p2 = player_type_p2
        self.time_limit_p1 = time_limit_p1
        self.time_limit_p2 = time_limit_p2
        self.heuristic_type_p1 = heuristic_type_p1
        self.heuristic_type_p2 = heuristic_type_p2

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

    @classmethod
    def from_default(cls):
        """
        Sets defaults config values for the program.
        :return: None
        """
        return Config(cls.DEFAULT_LAYOUT, cls.DEFAULT_MOVE_LIMIT,
                      cls.DEFAULT_PLAYER_TYPE_P1, cls.DEFAULT_PLAYER_TYPE_P2,
                      cls.DEFAULT_TIME_LIMIT_P1, cls.DEFAULT_TIME_LIMIT_P2,
                      cls.DEFAULT_HEURISTIC_TYPE_P1, cls.DEFAULT_HEURISTIC_TYPE_P2)
