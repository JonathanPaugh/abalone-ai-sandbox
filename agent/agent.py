import random

from agent.state_generator import StateGenerator
from core.move import Move


class Agent:
    def find_next_move(self, board, player) -> Move:
        moves = StateGenerator.enumerate_board(board, player.value)
        boards = StateGenerator.generate(board, moves) # TODO: Look at board outcomes, get heuristic values from each and return the move that lead to best outcome
        return random.choice(moves)