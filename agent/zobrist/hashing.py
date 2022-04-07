
from core.hex import Hex
from agent.zobrist.setup import zobrist_table, cell_table


def _get_piece_mask(cell, cell_state):
    return zobrist_table[_hash_piece(cell, cell_state)]

def _hash_piece(cell, cell_state):
    return cell_table[cell] * cell_state.value

def create_board_hash(board):
    """
    Creates a Zobrist hash with the given board.
    """
    board_hash = 0
    for cell, cell_state in board.enumerate_nonempty():
        board_hash ^= _get_piece_mask(cell, cell_state)
    return board_hash

def update_board_hash(hash, board, move):
    """
    Updates a Zobrist hash with the given move.
    Foregoes move validation in favor of speed.
    """
    move_tail = move.get_back() or move.selection.start
    move_cells = move.get_cells()
    move_targets = move.get_destinations()
    attacker_color = board[move_tail] if move_tail in board else None

    for cell in move_cells:
        hash ^= _get_piece_mask(cell, attacker_color)

    for target in move_targets:
        hash ^= _get_piece_mask(target, attacker_color)

    if not move.is_inline():
        return hash

    move_dest = move.get_front_target()
    defender_color = board[move_dest] if move_dest in board else None

    if defender_color is not None:
        hash ^= _get_piece_mask(move_dest, defender_color)

        push_dest = move_dest
        push_content = defender_color
        while push_content is not None:
            push_dest = Hex.add(push_dest, move.direction.value)
            push_content = board[push_dest] if push_dest in board else None

        if push_content is not None:
            hash ^= _get_piece_mask(push_dest, defender_color)

    return hash
