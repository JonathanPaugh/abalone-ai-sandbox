"""
Contains helpers for app-specific color transformations.
"""

import ui.view.colors.palette as palette

COLORMAP_DARKEN = {
    palette.COLOR_LIGHTBLUE: palette.COLOR_BLUE,
    palette.COLOR_BLUE: palette.COLOR_DARKBLUE,
    palette.COLOR_DARKBLUE: palette.COLOR_BLACK,
    palette.COLOR_LIGHTRED: palette.COLOR_RED,
    palette.COLOR_RED: palette.COLOR_DARKRED,
    palette.COLOR_DARKRED: palette.COLOR_BLACK,
    palette.COLOR_CYAN: palette.COLOR_TURQUOISE,
    palette.COLOR_TURQUOISE: palette.COLOR_TEAL,
    palette.COLOR_TEAL: palette.COLOR_BLACK,
    palette.COLOR_LAVENDER: palette.COLOR_PURPLE,
    palette.COLOR_PURPLE: palette.COLOR_VIOLET,
    palette.COLOR_VIOLET: palette.COLOR_BLACK,
    palette.COLOR_SILVER: palette.COLOR_GRAY,
    palette.COLOR_GRAY: palette.COLOR_DARKGRAY,
    palette.COLOR_DARKGRAY: palette.COLOR_CHARCOAL,
    palette.COLOR_CHARCOAL: palette.COLOR_BLACK,
}

COLORMAP_LIGHTEN = {
    palette.COLOR_BLUE: palette.COLOR_LIGHTBLUE,
    palette.COLOR_DARKBLUE: palette.COLOR_BLUE,
    palette.COLOR_RED: palette.COLOR_LIGHTRED,
    palette.COLOR_DARKRED: palette.COLOR_RED,
    palette.COLOR_TURQUOISE: palette.COLOR_CYAN,
    palette.COLOR_TEAL: palette.COLOR_TURQUOISE,
    palette.COLOR_PURPLE: palette.COLOR_LAVENDER,
    palette.COLOR_VIOLET: palette.COLOR_PURPLE,
    palette.COLOR_SILVER: palette.COLOR_WHITE,
    palette.COLOR_GRAY: palette.COLOR_SILVER,
    palette.COLOR_DARKGRAY: palette.COLOR_GRAY,
    palette.COLOR_CHARCOAL: palette.COLOR_DARKGRAY,
    palette.COLOR_BLACK: palette.COLOR_CHARCOAL,
}

def darken_color(color):
    """
    Selects the darkened shade of the given color.
    Returns the color provided if a darker shade has not been registered.
    :param color: a str
    :return: a str
    """
    return (COLORMAP_DARKEN[color]
        if color in COLORMAP_DARKEN
        else color)

def lighten_color(color):
    """
    Selects the lightened shade of the given color.
    Returns the color provided if a lighter shade has not been registered.
    :param color: a str
    :return: a str
    """
    return (COLORMAP_LIGHTEN[color]
        if color in COLORMAP_LIGHTEN
        else color)
