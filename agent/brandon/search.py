from random import choice

from core.board import Board
from core.color import Color
from agent.state_generator import StateGenerator


class Search:

    def start(self, board: Board, color: Color, on_find: callable):
        moves = StateGenerator.enumerate_board(board, color)
        on_find(choice(moves))
