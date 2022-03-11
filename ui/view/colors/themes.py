from core.color import Color
import colors.palette as palette

THEME_DEFAULT = {
    Color.WHITE: palette.COLOR_BLUE,
    Color.BLACK: palette.COLOR_RED,
    "background": palette.COLOR_WHITE,
    "board_cell": palette.COLOR_SILVER,
}

THEME_MONOCHROME = {
    Color.WHITE: palette.COLOR_SILVER,
    Color.BLACK: palette.COLOR_CHARCOAL,
    "background": palette.COLOR_BROWN,
    "board_cell": palette.COLOR_SAND,
}

THEME_DARK = {
    Color.WHITE: palette.COLOR_TURQUOISE,
    Color.BLACK: palette.COLOR_PURPLE,
    "background": palette.COLOR_DARKGRAY,
    "board_cell": palette.COLOR_CHARCOAL,
}
