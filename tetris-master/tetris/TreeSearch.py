from tetris.util import Point, Dimension
from tetris.piece import random_piece
import GameState
import tetris.heuristic as th
import math

PSEUDO_INFINITY = 10000000000.0


def max_search(self, node, depth, max_depth):
    """ Search method that maximizes your score. """
    depth += 1
    child_states = node.getNextStates()

    if(depth >= max_depth) or (len(child_states) == 0):
        return th.heuristic(node)

    max_val = -PSEUDO_INFINITY

    for child in child_states:
        child_node = GameState.GameNode(
            child.getGrid(), child.getPiece(), child.getNextPiece(), child.getActions())
        max_val = max(max_val, max_search(self, child_node, depth, max_depth))

    return max_val
