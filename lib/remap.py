"""
Remap math logic.
"""


def remap(value, old_min, old_max, new_min, new_max):
    """
    Remaps a `value` between `new_min` and `new_max` based on where it was between `old_min` and `old_max`
    :param value:
    :param old_min: a float
    :param old_max: a float
    :param new_min: a float
    :param new_max: a float
    :return: a float
    """
    return (((value - old_min) * (new_max - new_min)) / (old_max - old_min)) + new_min


def remap_01(value, old_min, old_max):
    """
    Remaps a `value` between 0 and 1 based on where it was between `old_min` and `old_max`
    :param value:
    :param old_min: a float
    :param old_max: a float
    :return: a float
    """
    return remap(value, old_min, old_max, 0, 1)
