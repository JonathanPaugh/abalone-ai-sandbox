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
        """
        Forces the thread to stop by interrupting the search.
        Blocks thread until thread is completely done running.
        """
        self.stopped.set()
        self.search.interrupt = True
        self.join()

    def run(self):
        """
        Runs the thread and the search.
        Calls on_complete() after if search not interrupted.
        """
        self.running = True
        self.search.alpha_beta(self.board, self.player, self.on_find)
        self.running = False

        if not self.search.interrupt:
            self.on_complete()
