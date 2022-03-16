"""
Contains helpers for composing functions.
"""

def _exhaust(generator):
    """
    Exhausts the given generator with disregard for return values.
    :param generator: a generator
    """
    for _ in generator:
        pass

def compose_fns(*fns):
    """
    Composes multiple functions into a single callback.
    :param *fns: the functions to compose
    :return: a function
    """
    return lambda: _exhaust((fn() for fn in fns if fn))
