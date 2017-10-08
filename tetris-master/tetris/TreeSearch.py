import time
import math
import random
import copy
import numpy as np
from tetris.util import Point, Dimension
from tetris.piece import random_piece
import GameState
import tetris.heuristic as th

PSEUDO_INFINITY = 10000000000.0


def max_search(node, depth, max_depth):
    """Search method that maximizes your score."""
    depth += 1
    child_nodes = node.getChildren()

    if(depth >= max_depth) or (node.state.end_of_game is True):
        return th.heuristic(node)

    max_val = -PSEUDO_INFINITY
    for child in child_nodes:
        max_val = max(max_val, max_search(child, depth, max_depth))

    return max_val


class GameNode(object):
    """GameNode contains all vital information about a game state."""
    hashtable = [0] * 1000000  # hashtable to avoid duplicate children
    children = []  # hold every child state

    def __init__(self, state, parent=None, action=None):
        self.state = state
        self.action = action
        self.parent = parent
        self.children = []
        self.wins = 0
        self.plays = 0
        self.UCB = 0

    def getChildren(self):
        for translation in range(-5, 6, 1):  # Translations relative to the middle of the board
            for rotation in range(0, 4, 1):  # Number of rotations
                # Simulate the game by dong a few rotations and translations: get the new state (for each performed move)
                action = (rotation, translation)
                new_state = GameState.TetrisGame(self.state.grid, self.state.curr_piece, self.state.next_piece, rotation, translation)
                child = GameNode(new_state, self, action)
                self.children.append(child)

                # Get a state string (in order to hash it)
                # new_state_grid = new_state.getGrid()
                # new_state_string = self.gridToString(new_state_grid)
                # Calculate the hash value
                # hash_val = abs(hash(new_state_string))
                # Check for hash collision
                # if (self.hashtable[hash_val % 1000000] == 0):
                #     self.hashtable[hash_val % 1000000] = 1
                #     child = GameNode(new_state.getGrid(), piece, next_piece, new_state.getActions())
                #     self.children.append(child)

        return self.children


    def printGrid(self):
        state = [[0 for i in xrange(GameState.GridSize.width)]
                 for i in xrange(GameState.GridSize.height)]
        for x in xrange(GameState.GridSize.width):
            for y in xrange(GameState.GridSize.height):
                state[y][x] = self.state.grid[x][y]
        for row in state:
            print(row)
        print("\n")

    def getGrid(self):
        return self.state.grid

    def getAction(self):
        return self.action

    def gridToString(self):
        state_string = ""
        for x in xrange(GameState.GridSize.width):
            for y in xrange(GameState.GridSize.height):
                state_string += str(self.state.grid[x][y])
        return state_string

    def gridToStringPretty(self):
        state_string = ""
        state = [[0 for i in xrange(GameState.GridSize.width)]
                 for i in xrange(GameState.GridSize.height)]
        for x in xrange(GameState.GridSize.width):
            for y in xrange(GameState.GridSize.height):
                state[y][x] = self.state.grid[x][y]
        for row in state:
            state_string += str(row)
            state_string += "\n"
        return state_string

    def __str__(self):
        if(self.parent is None):
            return ("ROOT" + "\nState: " + str(self.gridToStringPretty()) + "EOG:" + str(self.state.end_of_game) + "\nPlays: " + str(self.plays) + "\nWins: " + str(self.wins) + "\n")
        else:
            return ("State:" + str(self.gridToStringPretty()) + "Action: " + str(self.action) + "\nEOG:" + str(self.state.end_of_game) + "\nPlays: " + str(self.plays) + "\nWins: " + str(self.wins) + "\n")


class MonteCarloTreeSearch(object):
    """Monte Carlo Tree Search for Tetris."""

    def __init__(self, game_state):
        # MCTS parameters
        self.max_length = 10  # max search length
        self.max_iter = 20
        self.max_time = 1.0
        self.max_actions = 200
        self.time_start = 0
        self.root = GameNode(game_state)
        self.root.parent = None
        self.root.children = []
        self.root.plays = 1
        self.C = 1.4

    def UCB(self, node, child, C):
        """Calculation of Upper-Confidence Bound for Trees 1."""
        return child.wins + self.C * math.sqrt(math.log(node.plays) / child.plays)

    def UCB_sample(self, node):
        """Sampling of tree nodes based on their UCB1 values."""
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
        """This function expands the tree by checking if all the possible actions have been performed."""
        print("-------- Expansion --------")
        actions_taken = [child.action for child in node.children]
        legal_actions = node.getLegalActions()
        actions_left = [
            action for action in legal_actions if action not in actions_taken]

        if(len(actions_left) == 0):
            return node, random.choice(node.children)

        rand_action = random.choice(actions_left)

        next_state = node.state.generateSuccessor(rand_action)
        child = GameNode(next_state)
        child.parent = node
        child.action = rand_action
        child.children = []
        node.children.append(child)

        return node, child

    def selection(self):
        """This function analyzes the tree, expands it if needed, and chooses the best path to follow based on UCB."""
        print("-------- Selection --------")
        node = self.root
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
        is greater than one, the tree root."""
        print("-------- Simulation --------")
        state = child.state
        points = 0
        itr = 1

        elapsed = time.time() - self.time_start
        while (itr <= self.max_length) and (elapsed < 0.8):
            # Get all the possible actions, and choose a random one. Predict the next state and evaluate it with the heuristic function
            legal_actions = state.getLegalActions(state)
            action = random.choice(legal_actions)
            state = state.generateSuccessor(action)
            points += state.getPoints(child.state, state, self.root.state)

            itr += 1
            elapsed = time.time() - self.time_start

        if(points > 0):
            child.wins += 1

        return child

    def backpropagation(self, child):
        """Function to propagate the score from the leafs to the tree root."""
        print("-------- Backpropagation --------")
        node = child
        while(node.parent is not None):
            parent = node.parent
            parent.plays += 1
            parent.wins += node.wins
            node = parent

        return node

    def MCTS_sample(self):
        """Most important function of MCTS. It triggers the process of selection, simulation and backpropagation."""
        node = self.selection()
        node = self.simulation(node)
        root = self.backpropagation(node)
        return root

    def play(self, game_state):
        """Monte Carlo Tree Search"""
        print("\n*********  MCTS *********")

        self.time_start = time.time()
        elapsed = 0
        actions = game_state.getLegalActions()
        best_action = random.choice(actions)

        if (self.root.state != game_state):
            self.root = GameNode(game_state)
            self.root.parent = None
            self.root.children = []
            self.root.plays = 1

        itr = 0
        while(itr < self.max_iter) and (elapsed < self.max_time):
            self.root = self.MCTS_sample()
            itr += 1
            elapsed = time.time() - self.time_start

        next_node = self.UCB_sample(self.root)
        best_action = next_node.action

        return best_action


""" To instantiate this class, and play the game with MCTS, add the following snippet to the game code:

    if(gameState.getRound() == 0):
        mcts = MonteCarloTreeSearch(gameState)
    mcts.play(game_state)

"""
