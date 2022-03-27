from ui.constants import FPS
import threading

class AgentThread(threading.Thread):
    def __init__(self, search, board, player, on_find, on_complete):
        super().__init__()
        self.stopped = threading.Event()
        self.daemon = True
        self.running = False

        self.search = search
        self.board = board
        self.player = player

        self.on_find = on_find
        self.on_complete = on_complete

    def stop(self):
        self.stopped.set()
        self.search.interrupt = True
        self.join()

    def run(self):
        self.running = True
        self.search.alpha_beta(self.board, self.player, self.on_find)
        self.running = False

        if not self.search.interrupt:
            self.on_complete()
