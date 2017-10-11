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
    child_nodes = node.getFutureStates()

    if(depth >= max_depth) or (node.state.end_of_game is True):
        return th.heuristic(node.state.getState())

    max_val = -PSEUDO_INFINITY
    for child in child_nodes:
        max_val = max(max_val, max_search(child, depth, max_depth))

    return max_val


class GameNode(object):
    """GameNode contains all vital information about a game state."""

    def __init__(self, state, parent=None, action=None):
        self.hashtable = [0] * 10000  # hashtable to avoid duplicate children
        self.state = state # contains the copy of the game state
        self.action = action # the action that led to this state
        self.parent = parent # parent node reference
        self.visited_states = []
        self.future_states = []
        self.wins = 0
        self.plays = 0
        self.UCB = 0
        self.heuristic = th.heuristic(self.getState())
        self.cleared_rows = state.cleared_rows # THIS IS THE NUMBER OF CLEARED ROWS FROM PARENT NODE --> THIS NODE (that is, only one step)

    def getFutureStates(self):
        if(len(self.future_states) == 0):
            # Translations relative to the middle of the board
            for translation in range(-5, 6, 1):
                for rotation in range(0, 4, 1):  # Number of rotations
                    # Simulate the game by dong a few rotations and translations: get the new state (for each performed move)
                    new_state = GameState.TetrisGame(self.state.grid, self.state.curr_piece, self.state.next_piece, rotation, translation)
                    action = (rotation, translation)
                    child = GameNode(new_state, self, action)

                    # hashing preprocess
                    child_grid_string = child.gridToString()
                    hash_value = abs(hash(child_grid_string))

                    # if this child has not been added yet, append it to the children list
                    if (self.hashtable[hash_value % 10000] == 0):
                        self.hashtable[hash_value % 10000] = 1
                        self.future_states.append(child)

        return self.future_states

    def getState(self):
        state = [[0 for i in xrange(GameState.GridSize.width)]
                 for i in xrange(GameState.GridSize.height)]
        for x in xrange(GameState.GridSize.width):
            for y in xrange(GameState.GridSize.height):
                state[y][x] = self.state.grid[x][y]
        return state

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
            return ("ROOT" + "\nState\n" + str(self.gridToStringPretty()) + "EOG:" + str(self.state.end_of_game) + "\nPlays: " + str(self.plays) + "\nWins: " + str(self.wins) + "\nHeuristic: " + str(self.heuristic))
        else:
            return ("State:\n" + str(self.gridToStringPretty()) + "Action: " + str(self.action) + "\nEOG:" + str(self.state.end_of_game) + "\nPlays: " + str(self.plays) + "\nWins: " + str(self.wins) + "\nHeuristic: " + str(self.heuristic))


class MonteCarloTreeSearch(object):
    """Monte Carlo Tree Search for Tetris."""

    def __init__(self, root_node):
        # MCTS parameters
        self.max_simulations = 5  # max search length
        self.max_iter = 20
        self.max_time = 2.0
        self.time_start = 0
        self.root = root_node
        self.root.parent = None
        self.root.plays = 1
        self.C = 1

    def UCB(self, node, child):
        """Calculation of Upper-Confidence Bound for Trees 1."""
        return child.wins + self.C * math.sqrt(math.log(node.plays) / child.plays)

    def UCB_sample(self, node):
        """Sampling of tree nodes based on their UCB1 values."""
        print("-------- UCB sampling --------")
        weights = np.zeros(len(node.visited_states))
        i = 0
        for child in node.visited_states:
            w_i = self.UCB(node, child)
            weights[i] = w_i
            i += 1
        sum_weights = np.sum(weights)
        if(sum_weights != 0):
            weights /= sum_weights
            i = 0
            for child in node.visited_states:
                child.UCB = weights[i]
                i += 1
        idx_max = np.argmax(weights)
        return node.visited_states[idx_max]

    def expansion(self, node):
        """This function expands the tree by checking if all the possible actions have been performed."""
        # print("-------- Expansion --------")
        unexplored_states = [child for child in node.future_states if child not in node.visited_states]
        if(len(unexplored_states) == 0):
            return node, random.choice(node.visited_states)
        child = random.choice(unexplored_states)
        node.visited_states.append(child)
        return node, child

    def selection(self):
        """This function analyzes the tree, expands it if needed, and chooses the best path to follow based on UCB."""
        print("-------- Selection --------")
        node = self.root
        future_states = node.getFutureStates()

        if(len(node.visited_states) < len(future_states)):
        # print(node)
            _, node = self.expansion(self.root)
        else:
            # Let's search for a leaf in the tree
            while(len(node.visited_states) > 0):
                if(len(node.visited_states) == len(future_states)):
                    # If we have explored all possible future states, pick the "best one"
                    node = self.UCB_sample(node)
                else:
                    _, node = self.expansion(node)
                future_states = node.getFutureStates()

        node.plays += 1
        return node


    def simulation(self, node):
        """Given an initial state, this function simulates a random playout for a given time. If the score obtained 
        is greater than one, the tree root."""
        print("-------- Simulation --------")
        points = 0
        itr = 1
        child = node
        while (itr <= self.max_simulations):
            # Get all the possible actions, and choose a random one. Predict the next state and evaluate it with the heuristic function
            children = child.getFutureStates()
            if(len(children) > 0):
                child = random.choice(children)
            else:
                break
            points += child.heuristic   # Run heuristic here
            itr += 1

        print("    Simulations ran = " + str(itr))
        print("    points/max_sims = " + str(points/self.max_simulations))
        if (points/self.max_simulations > -30):
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

    def run(self):
        """Monte Carlo Tree Search"""
        print("\n\n************  MCTS ************")

        self.time_start = time.time()
        elapsed = 0

        future_states = self.root.getFutureStates()
        print("    Length of future nodes list = " + str(len(future_states)))
#        best_state = random.choice(future_states)

        itr = 0
        while(itr < self.max_iter) and (elapsed < self.max_time):
            print("##### Iteration " + str(itr) + " #####")
            # self.root = self.MCTS_sample()
            node = self.selection()
            elapsed = time.time() - self.time_start
            print("    Time elapsed = " + str(elapsed))

            node = self.simulation(node)
            elapsed = time.time() - self.time_start
            print("    Time elapsed = " + str(elapsed))

            root = self.backpropagation(node)
            elapsed = time.time() - self.time_start
            print("    Time elapsed = " + str(elapsed))
            itr += 1

        best_state = self.UCB_sample(self.root)
        print("    Number of nodes explored near root = " + str(len(self.root.visited_states)))
        print("    Best future state:")
        print(best_state)
        print("    Best action to take = " + str(best_state.action))

        return best_state


""" To instantiate this class, and play the game with MCTS, add the following snippet to the game code:

    if(gameState.getRound() == 0):
        mcts = MonteCarloTreeSearch(gameState)
    mcts.run(game_state)

"""
