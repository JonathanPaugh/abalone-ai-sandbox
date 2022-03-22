"""
Clamp math logic.
"""


def clamp(a, b, v):
    """
    Clamps a value `v` between `a` and `b`
    :param a: a float
    :param b: a float
    :param v: a float
    :return: a float
    """
    return max(a, min(v, b))

def clamp_01(v):
    """
    Clamps a value `v` between 0 and 1
    :param v: a float
    :return: a float
    """
    return clamp(0, 1, v)