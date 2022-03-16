from math import inf


class Anim:

    duration = inf

    def __init__(self, duration=inf, delay=0, loop=False, target=None, on_start=None, on_end=None):
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
        return max(0, self._time)

    @property
    def done(self):
        return self._done

    @property
    def target(self):
        return self._target

    def end(self):
        self._done = True
        if self.on_end:
            self.on_end()

    def update(self):
        if self.done:
            return -1

        if self._time == 0 and self.on_start:
            self.on_start()

        self._time += 1
        if self._duration and self._time >= self._duration and not self._loop:
            self.end()

        if self._time < 0:
            return 0

        return self._time
