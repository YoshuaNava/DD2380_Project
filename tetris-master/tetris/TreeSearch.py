import time
import math
import random
import numpy as np
from tetris.util import Point, Dimension
from tetris.piece import random_piece
import GameState
import tetris.heuristic as th

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


class Node():
    def __init__(self, state=None, parent=None, action=None):
        self.state = state
        self.parent = parent
        self.children = []
        self.action = action
        self.wins = 0
        self.plays = 0
        self.UCB = 0

    def __str__(self):
        if(self.parent is None):
            return ("ROOT" + "\nState: " + str(self.state) + "Plays: " + str(self.plays) + "\nWins: " + str(self.wins) + "\n")
        else:
            return ("State:" + str(self.state) + "\nAction: " + str(self.action) + "\nPlays: " + str(self.plays) + "\nWins: " + str(self.wins))


class MonteCarloTreeSearch:
    def __init__(self, gameState):
        # MCTS parameters
        self.max_length = 10  # max search length
        self.max_iter = 20
        self.max_time = 1.0
        self.max_actions = 200
        self.time_start = 0
        self.root = Node(gameState)
        self.root.parent = None
        self.root.children = []
        self.root.plays = 1
        self.C = 1.4


    def UCB(self, node, child, C):
        """Calculation of Upper-Confidence Bound for Trees 1"""
        return child.wins + self.C * math.sqrt(math.log(node.plays) / child.plays)


    def UCB_sample(self, node):
        """Sampling of tree nodes based on their UCB1 values"""
        print("-------- UCB sampling --------")
        weights = np.zeros(len(node.children))
        i = 0
        for child in node.children:
            w = self.UCB(self, node, child)
            weights[i] = w
            i += 1
        sum_weights = np.sum(weights)
        if(sum_weights != 0):
            weights /= sum_weights
            i = 0
            for child in node.children:
                child.UCB = weights[i]
                i += 1
        idx_max = np.argmax(weights)
        return node.children[idx_max]


    def expansion(self, node):
        """This function expands the tree by checking if all the possible actions have been performed"""
        #    #print("-------- Expansion --------")
        actions_taken = [child.action for child in node.children]
        legal_actions = node.getLegalActions()
        actions_left = [action for action in legal_actions if action not in actions_taken]

        if(len(actions_left) == 0):
            return node, random.choice(node.children)

        rand_action = random.choice(actions_left)

        next_state = node.state.generateSuccessor(rand_action)
        child = Node(next_state)
        child.parent = node
        child.action = rand_action
        child.children = []
        node.children.append(child)

        return node, child


    def selection(self, root):
        """This function analyzes the tree, expands it if needed, and chooses the best path to follow based on UCB"""
        print("-------- Selection --------")
        node = root
        legal_actions = node.getLegalActions(node.state)
        expanded = False
        
        if(len(node.children) < len(legal_actions)):
            # If we haven't explored all possible actions, choose one unexplored action randomly and expand the tree
            _, node = self.expansion(node)
        else:

            while(len(node.children) > 0):
                legal_actions = node.getLegalActions()
                if(len(node.children) == len(legal_actions)):
                    # If we have explored all possible actions, pick the "best one"
                    node = self.UCB_sample(node)
                else:
                    # If we haven't explored all possible actions, choose one unexplored action randomly and expand the tree
                    _, node = self.expansion(node)
                    expanded = True

            if (not expanded):
                _, node = self.expansion(node)

        node.plays += 1

        return node


    def simulation(self, child):
        """Given an initial state, this function simulates a random playout for a given time. If the score obtained 
        is greater than one, the tree root"""
        print("-------- Simulation --------")
        state = child.state
        points = 0
        itr = 1

        elapsed = time.time() - self.time_start
        while (itr <= self.max_length) and (elapsed < 0.8):
            legal_actions = state.getLegalActions(state)
            action = random.choice(legal_actions)
            points = points + state.getPoints(child.state, state, self.root.state)
            state = state.generateSuccessor(action)
            itr += 1
            elapsed = time.time() - self.time_start

        if(points > 0):
            child.wins += 1

        return child


    def backpropagation(self, child):
        """Function to propagate the score from the leafs to the tree root"""
        print("-------- Backpropagation --------")
        node = child
        while(node.parent is not None):
            parent = node.parent
            parent.plays += 1
            parent.wins += node.wins
            node = parent

        return node


    def MCTS_sample(self, root):
        """Most important function of MCTS. It triggers the process of selection, simulation and backpropagation"""
        node = self.selection(root)
        node = self.simulation(node)
        root = self.backpropagation(node)
        return root
