"""
Generic standard-issue interpolation logic.
"""

def lerp(a, b, t):
    """
    Interpolates between `a` and `b` at `t`%.
    :param a: a float
    :param b: a float
    :param t: a float between 0 and 1, inclusive
    :return: a float
    """
    return a * (1 - t) + b * t
