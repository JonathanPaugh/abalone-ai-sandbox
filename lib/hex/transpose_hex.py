from math import sqrt
from lib.hex.axial_round import axial_round

def hex_to_point(cell, radius):
    q, r = cell
    size = radius * 2 / sqrt(3)
    x = size * (sqrt(3) * q + sqrt(3) / 2 * r) - (radius * 3)
    y = size * 3 / 2 * (r + 1 / 2)
    return x, y

def point_to_hex(point, radius):
    x, y = point
    q = (sqrt(3) / 3 * x - 1 / 3 * y) / radius
    r = (2 / 3 * y) / radius
    return axial_round(q, r)
