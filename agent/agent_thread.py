from ui.constants import FPS
import threading

class AgentThread(threading.Thread):
    def __init__(self, search, board, player, on_find_move):
        super().__init__()
        self.stopped = threading.Event()
        self.daemon = True

        self.on_find_move = on_find_move
        self.search = search
        self.board = board
        self.player = player

    def stop(self):
        self.stopped.set()
        self.search.interrupt = True
        self.join()

    def run(self):
        move = self.search.find_next_move(self.board, self.player)
        self.on_find_move(move)

