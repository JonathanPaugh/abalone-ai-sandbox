from ui.constants import FPS
import threading

class AgentThread(threading.Thread):
    def __init__(self, agent, board, player, on_find_move):
        super().__init__()
        self.stopped = threading.Event()
        self.daemon = True

        self.on_find_move = on_find_move
        self.agent = agent
        self.board = board
        self.player = player

    def stop(self):
        self.stopped.set()
        print("STOP")
        self.agent.interrupt = True
        self.join()

    def run(self):
        self.on_find_move(self.agent.find_next_move(self.board, self.player))

