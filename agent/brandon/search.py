from math import inf
from time import time, sleep
from copy import deepcopy
from core.board import Board
from core.color import Color
from agent.zobrist import Zobrist
from agent.brandon.transposition_table import TranspositionTable
from agent.state_generator import StateGenerator
from ui.constants import FPS
from ui.debug import Debug


class Search:
    """
    An interface around Abalone search logic.
    """

    @staticmethod
    def _estimate_move_score(board, move):
        WEIGHT_SUMITO = 10 # consider sumitos first
        return (len(move.get_cells())
            + WEIGHT_SUMITO * move.is_sumito(board))

    @classmethod
    def _order_moves(cls, board, moves):
        return sorted(moves, key=lambda move: cls._estimate_move_score(board, move), reverse=True)

    def __init__(self):
        self.heuristic = None
        self._stopped = False
        self._paused = False
        self._transposition_table = {}
        self.__debug_num_tt_reads = 0
        self.__debug_num_tt_hits = 0

    @property
    def stopped(self):
        return self._stopped

    def start(self, board: Board, color: Color, depth: int = 2, on_find: callable = None):
        """
        Starts the search.
        :return: a bool denoting whether the search was completed or not
        """
        self._stopped = False
        try:
            self._search(board, color, depth, on_find)
            exhausted = True
        except StopIteration:
            exhausted = False

        Debug.log(f"search result: {'exhausted' if exhausted else 'interrupted'}")

        tt_hit_rate = self.__debug_num_tt_hits / (self.__debug_num_tt_reads or 1)
        tt_hit_percent = tt_hit_rate * 100
        Debug.log(f"transposition table size: {len(self._transposition_table)} nodes")
        Debug.log(f"transposition table hit rate:"
            f" {self.__debug_num_tt_hits}/{self.__debug_num_tt_reads}"
            f" ({tt_hit_percent:.2f}%)")

        return exhausted

    def stop(self):
        """
        Stops the search.
        """
        self._paused = False
        self._stopped = True

    def toggle_paused(self):
        """
        Pauses or unpauses the search.
        """
        self._paused = not self._paused

    def _search(self, board: Board, color: Color, depth: int, on_find: callable = None):
        moves = StateGenerator.enumerate_board(board, color)
        moves = self._order_moves(board, moves)
        root_hash = Zobrist.create_board_hash(board)

        for d in range(1, depth + 1):
            alpha = -inf
            time_start = time()

            for move in moves:
                self._handle_interrupts()
                move_board = deepcopy(board)
                move_board.apply_move(move)
                move_hash = Zobrist.update_board_hash(root_hash, board, move)

                move_score = -self._negamax(move_board, move_hash, color, d - 1, -inf, -alpha, -1)
                if move_score > alpha:
                    alpha = move_score
                    if on_find:
                        on_find(move)
                    Debug.log(f"new best move {move}/{move_score:.2f}")

            Debug.log(f"complete search at depth {d} in {time() - time_start:.2f}s")

    def _negamax(self, board, board_hash, color, depth, alpha, beta, perspective):
        self._handle_interrupts()

        self.__debug_num_tt_reads += 1
        cached_entry = (self._transposition_table[board_hash]
            if board_hash in self._transposition_table
            else None)

        if cached_entry:
            self.__debug_num_tt_hits += 1
            if cached_entry.type == TranspositionTable.EntryType.PV:
                return cached_entry.score
            elif cached_entry.type == TranspositionTable.EntryType.CUT:
                alpha = max(alpha, cached_entry.score)
            elif cached_entry.type == TranspositionTable.EntryType.ALL:
                beta = min(beta, cached_entry.score)

            if alpha >= beta:
                return cached_entry.score

        if depth == 0:
            return self.heuristic.call(board, color) * perspective

        alpha_old = alpha
        best_score = -inf
        best_move = None
        true_color = color if perspective == 1 else Color.next(color)

        moves = StateGenerator.enumerate_board(board, true_color)
        for move in moves:
            move_board = deepcopy(board)
            move_board.apply_move(move)
            move_hash = Zobrist.update_board_hash(board_hash, board, move)

            move_score = -self._negamax(move_board, move_hash, color, depth - 1, -beta, -alpha, -perspective)
            if move_score > best_score:
                best_score = move_score
                best_move = move

            alpha = max(alpha, best_score)
            if alpha >= beta:
                break

        if board_hash in self._transposition_table:
            cached_entry = self._transposition_table[board_hash]
        else:
            cached_entry = TranspositionTable.Entry()
            self._transposition_table[board_hash] = cached_entry

        cached_entry.score = best_score
        cached_entry.move = best_move
        cached_entry.depth = depth

        if best_score <= alpha_old:
            cached_entry.type = TranspositionTable.EntryType.ALL
        elif best_score >= beta:
            cached_entry.type = TranspositionTable.EntryType.CUT
        else:
            cached_entry.type = TranspositionTable.EntryType.PV

        return best_score

    def _handle_interrupts(self):
        while self._paused:
            sleep(1 / FPS)

        if self._stopped:
            raise StopIteration
