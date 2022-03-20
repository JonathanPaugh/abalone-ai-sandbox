import threading

class IntervalTimer(threading.Thread):
    def __init__(self, total_time: float, interval: float):
        threading.Thread.__init__(self)
        self.total_time = total_time
        self.interval = interval

        self.on_interval = None
        self.on_complete = None

        self.stopped = threading.Event()
        self.daemon = True

    def set_on_complete(self, on_complete):
        self.on_complete = on_complete

    def set_on_interval(self, on_interval):
        self.on_interval = on_interval

    def run(self):
        remaining_time = self.total_time
        while remaining_time > 0 and not self.stopped.wait(self.interval):
            remaining_time -= self.interval
            if self.on_interval:
                self.on_interval(self._clamp_01(remaining_time / self.total_time))

        if self.on_complete:
            self.on_complete()

    def _clamp_01(self, value: float) -> float:
        return max(0, min(value, 1))
