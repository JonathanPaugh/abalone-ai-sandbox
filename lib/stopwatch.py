from time import time_ns


def stopwatch(f) -> int:
    """
    Measures time a function takes to run.
    :param f: a Function.
    :return: a int of nanoseconds.
    """
    start = time_ns()
    f()
    return time_ns() - start
