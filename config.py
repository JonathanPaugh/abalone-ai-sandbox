
class Config:
    """
    Config defines the customization settings for the program.
    """

    DEFAULT_LAYOUT = "Standard"
    DEFAULT_GAME_MODE = "Human vs. Computer"
    DEFAULT_PLAYER_COLOR = "White"
    DEFAULT_MOVE_LIMIT_P1 = 50
    DEFAULT_MOVE_LIMIT_P2 = 50
    DEFAULT_TIME_LIMIT_P1 = 5
    DEFAULT_TIME_LIMIT_P2 = 5

    def __init__(self, layout, game_mode, player_color,
                 move_limit_p1, move_limit_p2,
                 time_limit_p1, time_limit_p2):
        self.layout = layout
        self.game_mode = game_mode
        self.player_color = player_color
        self.move_limit_p1 = move_limit_p1
        self.move_limit_p2 = move_limit_p2
        self.time_limit_p1 = time_limit_p1
        self.time_limit_p2 = time_limit_p2

    @classmethod
    def from_default(cls):
        """
        Sets defaults config values for the program.
        :return: None
        """
        return Config(cls.DEFAULT_LAYOUT, cls.DEFAULT_GAME_MODE, cls.DEFAULT_PLAYER_COLOR,
                      cls.DEFAULT_MOVE_LIMIT_P1, cls.DEFAULT_MOVE_LIMIT_P2,
                      cls.DEFAULT_TIME_LIMIT_P1, cls.DEFAULT_TIME_LIMIT_P2)
