from core.board_layout import BoardLayout


class Config:
    """
    Config defines the customization settings for the program.
    """

    DEFAULT_LAYOUT = BoardLayout.STANDARD
    DEFAULT_MOVE_LIMIT = 50
    DEFAULT_PLAYER_TYPE_P1 = "Human"
    DEFAULT_PLAYER_TYPE_P2 = "Computer"
    DEFAULT_TIME_LIMIT_P1 = 20
    DEFAULT_TIME_LIMIT_P2 = 5

    def __init__(self, layout, move_limit, player_type_p1, player_type_p2,  time_limit_p1, time_limit_p2):
        self.layout = layout
        self.move_limit = move_limit
        self.player_type_p1 = player_type_p1
        self.player_type_p2 = player_type_p2
        self.time_limit_p1 = time_limit_p1
        self.time_limit_p2 = time_limit_p2

    @classmethod
    def from_default(cls):
        """
        Sets defaults config values for the program.
        :return: None
        """
        return Config(cls.DEFAULT_LAYOUT, cls.DEFAULT_MOVE_LIMIT,
                      cls.DEFAULT_PLAYER_TYPE_P1, cls.DEFAULT_PLAYER_TYPE_P2,
                      cls.DEFAULT_TIME_LIMIT_P1, cls.DEFAULT_TIME_LIMIT_P2)
