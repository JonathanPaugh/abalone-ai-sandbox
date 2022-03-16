"""
Defines generic exponential easing functions.
May be expressed as a static class that inherits from an `Easing` abstract base class.
"""

def ease_in(t):
    """
    Applies an ease-in transform to the given value.
    :param t: a float denoting the time to transform
    :return: a float denoting the transformed time
    """
    return t * t

def ease_out(t):
    """
    Applies an ease-out transform to the given value.
    :param t: a float denoting the time to transform
    :return: a float denoting the transformed time
    """
    return -t * (t - 2)

def ease_in_out(t):
    """
    Applies an ease-in-out transform to the given value.
    :param t: a float denoting the time to transform
    :return: a float denoting the transformed time
    """
    return (ease_in(t * 2) / 2
        if t < 0.5
        else (ease_out(t * 2 - 1) + 1) / 2)
