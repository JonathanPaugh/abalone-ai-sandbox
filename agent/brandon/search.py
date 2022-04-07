"""
Defines common search logic for Brandon's agent.
"""

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

    @staticmethod
    def _is_quiescent(board):
        """
        Determines if the given board has adjacent opposing marbles.
        :param board: a Board
        """
        for cell, color in board.enumerate_nonempty():
            for neighbor in cell.neighbors_se():
                neighbor_color = board[neighbor] if neighbor in board else None
                if neighbor_color and neighbor_color != color:
                    return False
        return True

    @classmethod
    def _order_moves(cls, board, moves, best_move=None):
        if best_move:
            # list principal variation first
            return [best_move, *[move for move in moves if move != best_move]]

        return sorted(moves, key=lambda move: cls._estimate_move_score(board, move), reverse=True)

    def __init__(self):
        self.heuristic = None
        self._stopped = False
        self._paused = False
        self._transposition_table = {}
        self.__debug_num_tt_reads = 0
        self.__debug_num_tt_hits = 0
        self.__debug_num_nodes_enumerated = 0
        self.__debug_num_nodes_pruned = 0
        self.__debug_num_plies_expanded = 0

    @property
    def stopped(self):
        """
        Gets whether or not the search is stopped.
        :return: a bool
        """
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

        self.__print_debug_report(exhausted)
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
        if self._is_quiescent(board) and depth > 1:
            return self._search(board, color, depth=1, on_find=on_find)

        moves = StateGenerator.enumerate_board(board, color)
        self.__debug_num_nodes_enumerated += len(moves)

        root_hash = Zobrist.create_board_hash(board)
        best_move = None

        for d in range(1, depth + 1):
            time_start = time()
            alpha = -inf
            self.__debug_num_plies_expanded += 1

            moves = self._order_moves(board, moves, best_move)
            is_first_move = True

            for move in moves:
                self._handle_interrupts()
                move_board = deepcopy(board)
                move_board.apply_move(move)
                move_hash = Zobrist.update_board_hash(root_hash, board, move)

                move_score = -self._negascout(
                    board=move_board,
                    board_hash=move_hash,
                    color=color,
                    depth=d - 1,
                    alpha=alpha,
                    beta=inf,
                    perspective=-1,
                    is_pv=is_first_move
                )
                is_first_move = False

                if move_score > alpha:
                    alpha = move_score
                    best_move = move
                    if on_find:
                        on_find(move)
                    Debug.log(f"new best move {move}/{move_score:.2f}")

            Debug.log(f"complete search at depth {d} in {time() - time_start:.2f}s")

    def _negascout(self, board, board_hash, color, depth, alpha, beta, perspective, is_pv=False):
        if is_pv:
            return self._negamax(board, board_hash, color, depth, -beta, -alpha, perspective)

        move_score = self._negamax(board, board_hash, color, depth, -alpha - 1, -alpha, perspective)
        if alpha < move_score < beta:
            return self._negamax(board, board_hash, color, depth, -beta, -move_score, perspective)

        return move_score

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
        best_move = cached_entry.move if cached_entry else None
        true_color = color if perspective == 1 else Color.next(color)

        moves = StateGenerator.enumerate_board(board, true_color)
        moves = self._order_moves(board, moves, best_move)
        self.__debug_num_nodes_enumerated += len(moves)
        self.__debug_num_plies_expanded += 1

        is_first_move = True
        for move in moves:
            move_board = deepcopy(board)
            move_board.apply_move(move)
            move_hash = Zobrist.update_board_hash(board_hash, board, move)

            move_score = -self._negascout(
                board=move_board,
                board_hash=move_hash,
                color=color,
                depth=depth - 1,
                alpha=alpha,
                beta=beta,
                perspective=-perspective,
                is_pv=is_first_move
            )
            is_first_move = False

            if move_score > best_score:
                best_score = move_score
                best_move = move

            alpha = max(alpha, best_score)
            if alpha >= beta:
                self.__debug_num_nodes_pruned += len(moves) - moves.index(move) - 1
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

    def __print_debug_report(self, exhausted):
        Debug.log(f"search result: {'exhausted' if exhausted else 'interrupted'}")

        prune_rate = self.__debug_num_nodes_pruned / (self.__debug_num_nodes_enumerated or 1)
        prune_percent = prune_rate * 100
        Debug.log(f"nodes enumerated: {self.__debug_num_nodes_enumerated}")
        Debug.log(f"nodes pruned: {self.__debug_num_nodes_pruned} ({prune_percent:.2f}%)")

        tt_hit_rate = self.__debug_num_tt_hits / (self.__debug_num_tt_reads or 1)
        tt_hit_percent = tt_hit_rate * 100
        Debug.log(f"transposition table size: {len(self._transposition_table)} nodes")
        Debug.log(f"transposition table hit rate:"
            f" {self.__debug_num_tt_hits}/{self.__debug_num_tt_reads}"
            f" ({tt_hit_percent:.2f}%)")

        num_nodes_explored = self.__debug_num_nodes_enumerated - self.__debug_num_nodes_pruned
        branching_factor = self.__debug_num_nodes_enumerated / self.__debug_num_plies_expanded
        effective_branching_factor = num_nodes_explored / self.__debug_num_plies_expanded
        Debug.log("effective branching factor: "
                  f"{effective_branching_factor:.2f}/{branching_factor:.2f}")
