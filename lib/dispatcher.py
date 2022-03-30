from queue import Queue


class Dispatcher(Queue):
    def dispatch(self):
        while not self.empty():
            self.get()()

    def clear(self):
        self.queue.clear()