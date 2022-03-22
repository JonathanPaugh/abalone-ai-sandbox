import random

from agent.state_generator import StateGenerator
from core.board import Board
from core.color import Color
from core.move import Move


class Agent:
    def find_next_move(self, board: Board, player: Color) -> Move:
        moves = StateGenerator.enumerate_board(board, player)
        boards = StateGenerator.generate(board, moves) # TODO: Look at board outcomes, get heuristic values from each and return the move that lead to best outcome
        return random.choice(moves)

