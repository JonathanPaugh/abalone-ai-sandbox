"""
Defines a generic animation class.
"""

from math import inf


class Anim:
    """
    A generic animation class.
    """
    duration = inf

    def __init__(self, duration=inf, delay=0, loop=False, target=None, on_start=None, on_end=None):
        """
        :param duration: an int denoting how many updates the animation should run for
        :param delay: an int denoting how many updates to wait before starting the animation
        :param loop: a bool denoting if the animation should end once its duration expires
        :param target: an object to attach this animation to
        :param on_start: the callback to perform once the animation starts (for delays and queueing)
        :param on_end: the callback to perform once the animation ends
        """
        self._duration = min(self.duration, duration)
        self._delay = delay
        self._time = -delay
        self._loop = loop
        self._target = target
        self._done = False
        self.on_start = on_start
        self.on_end = on_end

    @property
    def time(self):
        """
        Gets how many updates the animation has performed (0 if delayed).
        :return: an int
        """
        return max(0, self._time)

    @property
    def done(self):
        """
        Gets whether or not the animation has completed.
        :return: a bool
        """
        return self._done

    @property
    def target(self):
        """
        Gets the animation's target.
        :return: an object
        """
        return self._target

    def end(self):
        """
        Ends the animation.
        """
        if self._done:
            return

        self._done = True
        if self.on_end:
            self.on_end()

    def update(self):
        """
        Updates the animation.
        :return: an int (generally) denoting how many updates the animation has performed
        """
        if self._done:
            return -1

        if self._time == 0 and self.on_start:
            self.on_start()

        self._time += 1
        if self._duration and self._time >= self._duration and not self._loop:
            self.end()

        if self._time < 0:
            return 0

        return self._time
