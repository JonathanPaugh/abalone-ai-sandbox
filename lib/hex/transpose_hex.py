"""
Contains logic for transposing hex coordinates.
"""

from math import sqrt

def hex_to_point(cell, radius):
    """
    Converts a hex coordinate to a position on-screen.
    :param cell: a tuple[float, float]
    :param radius: a float denoting the hexagon radius
    """
    q, r = cell
    size = radius * 2 / sqrt(3)
    x = size * (sqrt(3) * q + sqrt(3) / 2 * r) - (radius * 3)
    y = size * 3 / 2 * (r + 1 / 2)
    return x, y

def point_to_hex(point, radius):
    """
    Converts an on-screen position to a hex coordinate.
    :param point: a tuple[float, float]
    :param radius: a float denoting the hexagon radius
    """
    x, y = point
    q = (sqrt(3) / 3 * x - 1 / 3 * y) / radius
    r = (2 / 3 * y) / radius
    return axial_round(q, r)

def axial_round(x, y):
    """
    Rounds an axial hex coordinate.
    Adapted from https://observablehq.com/@jrus/hexround.
    :param x: a float
    :param y: a float
    :return: a tuple[float, float]
    """
    xgrid = round(x)
    ygrid = round(y)
    x -= xgrid
    y -= ygrid
    dx = round(x + 0.5 * y) * (x * x >= y * y)
    dy = round(y + 0.5 * x) * (x * x < y * y)
    return (xgrid + dx, ygrid + dy)
