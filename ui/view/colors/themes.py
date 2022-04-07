from dataclasses import dataclass
from enum import Enum, auto
from core.color import Color
import ui.view.colors.palette as palette


class ThemeColor(Enum):
    """
    Enumerates possible theme color names.
    """
    MARBLE_BLACK = auto()
    MARBLE_WHITE = auto()
    BOARD_CELL = auto()
    BOARD_BACKGROUND = auto()

@dataclass(frozen=True)
class Theme:
    """
    Models a theme.
    """
    name: str
    colors: dict

    def __post_init__(self):
        # sugar to avoid internal mappings
        self.colors[Color.BLACK] = self.colors[ThemeColor.MARBLE_BLACK]
        self.colors[Color.WHITE] = self.colors[ThemeColor.MARBLE_WHITE]

    def get_color_by_key(self, key):
        """
        Gets a color from the given key.
        :param key: a ThemeColor
        :return: a str
        """
        return self.colors[key] if key in self.colors else None

class ThemeLibrary(Enum):
    """
    Enumerates the list of application themes.
    """

    DEFAULT = Theme("Default (Blue/Red)", colors={
        ThemeColor.MARBLE_BLACK: palette.COLOR_BLUE,
        ThemeColor.MARBLE_WHITE: palette.COLOR_RED,
        ThemeColor.BOARD_CELL: palette.COLOR_GRAY_200,
        ThemeColor.BOARD_BACKGROUND: palette.COLOR_GRAY_400,
    })

    MONOCHROME = Theme("Monochrome (Black/White)", colors={
        ThemeColor.MARBLE_BLACK: palette.COLOR_CHARCOAL,
        ThemeColor.MARBLE_WHITE: palette.COLOR_SILVER,
        ThemeColor.BOARD_CELL: palette.COLOR_RED_200,
        ThemeColor.BOARD_BACKGROUND: palette.COLOR_RED_400,
    })

    @classmethod
    def get_theme_by_name(cls, name):
        """
        Gets a theme by its name.
        :param name: a str
        :return: a ThemeLibrary.value
        """
        return next((t for t in cls if t.value.name == name), None)

    def get_color_by_key(self, key):
        """
        Gets a color from the given key.
        :param key: a ThemeColor
        :return: a str
        """
        return self.value.get_color_by_key(key)
