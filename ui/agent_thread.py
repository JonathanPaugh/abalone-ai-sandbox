import threading

class AgentThread(threading.Thread):
    def __init__(self, agent, board, player, on_find_move):
        threading.Thread.__init__(self)
        self.stopped = threading.Event()
        self.daemon = True

        self.on_find_move = on_find_move
        self.agent = agent
        self.board = board
        self.player = player

    def stop(self):
        self.stopped.set()

    def run(self):
        while not self.stopped.is_set():
            self.on_find_move(self.agent.find_next_move(self.board, self.player))
