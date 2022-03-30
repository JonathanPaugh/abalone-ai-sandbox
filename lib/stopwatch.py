from time import time_ns


def stopwatch(f):
    """
    Measures time a function takes to run.
    :param f: a Function.
    :return: A int of nanoseconds.
    """
    start = time_ns()
    f()
    return time_ns() - start
