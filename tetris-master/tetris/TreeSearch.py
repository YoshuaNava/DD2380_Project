import time
import math
import random
import copy
import numpy as np
import operator
from tetris.util import Point, Dimension
from tetris.piece import random_piece
import GameState
import tetris.heuristic as th

PSEUDO_INFINITY = 10000000000.0

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
        if(parent is not None):
            self.state.updateScore()

        # self.cleared_rows = state.cleared_rows # THIS IS THE NUMBER OF CLEARED ROWS FROM PARENT NODE --> THIS NODE (that is, only one step)
        

    def getFutureStates(self):
        if(len(self.future_states) == 0):
            # Translations relative to the middle of the board
            for translation in range(-5, 6, 1):
                for rotation in range(0, 4, 1):  # Number of rotations
                    # Simulate the game by dong a few rotations and translations: get the new state (for each performed move)
                    new_state = GameState.TetrisGame(self.state.grid, self.state.curr_piece, self.state.next_piece, rotation, translation, self.state.level, self.state.lines, self.state.score)

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
            return ("ROOT" + "\nState\n" + str(self.gridToStringPretty()) + "EOG:" + str(self.state.end_of_game) + "\nPlays: " + str(self.plays) + "\nWins: " + str(self.wins) + "\nHeuristic: " + str(self.heuristic) + "\nGameScore: " + str(self.state.score))
        else:
            return ("State:\n" + str(self.gridToStringPretty()) + "Action: " + str(self.action) + "\nEOG:" + str(self.state.end_of_game) + "\nPlays: " + str(self.plays) + "\nWins: " + str(self.wins) + "\nHeuristic: " + str(self.heuristic) + "\nGameScore: " + str(self.state.score))


class MonteCarloTreeSearch(object):
    """Monte Carlo Tree Search for Tetris."""

    def __init__(self, root_node):
        # MCTS parameters
        self.max_iter = 15
        self.max_sims = 3
        self.max_time = 5.0
        self.time_start = 0
        self.root = root_node
        self.root.parent = None
        self.root.plays = 1
        self.C = 0.5

    def UCB(self, node, child):
        """Calculation of Upper-Confidence Bound for Trees 1."""
        return child.wins/child.plays + self.C * math.sqrt(math.log(node.plays) / child.plays)

    def UCB_sample(self, node):
        """Sampling of tree nodes based on their UCB1 values."""
        print("-------- UCB sampling --------")
        weights = np.zeros(len(node.visited_states))
        i = 0
        for i, child in enumerate(node.visited_states):
            weights[i] = self.UCB(node, child)

        print(weights)
        idx_max = np.argmax(weights)
        return node.visited_states[idx_max]

    def expansion(self, node):
        """This function expands the tree by checking if all the possible actions have been performed."""
        # print("-------- Expansion --------")
        unexplored_states = [child for child in node.future_states if child not in node.visited_states]
        child = random.choice(unexplored_states)
        child.getFutureStates()
        node.visited_states.append(child)
        return node, child

    def selection(self):
        """This function analyzes the tree, expands it if needed, and chooses the best path to follow based on UCB."""
        # print("-------- Selection --------")
        node = self.root
        # UCB sampling the future states
        while(len(node.visited_states)==len(node.future_states)):
            node = self.UCB_sample(node)
        # Expand tree
        if(len(node.visited_states)<len(node.future_states)):
            _, node = self.expansion(node)
        node.plays += 1
        return node

    def simulation(self, node):
        """Given an initial state, this function simulates a random playout for a given time. If the score obtained 
        is greater than one, the tree root."""
        # print("-------- Simulation --------")
        sim = 0
        child = node
        while (sim < self.max_sims):
            # Get all the possible actions, and choose a random one. Predict the next state and evaluate it with the heuristic function
            future_states = child.getFutureStates()
            if(len(future_states) > 0):
                # child = random.choice(future_states)   # Random policy
                max_val = -PSEUDO_INFINITY
                index = random.randint(0, len(future_states)-1)
                for i, state in enumerate(future_states):
                    if(max_val < state.heuristic):
                        max_val = state.heuristic
                        index = i
                child = future_states[index]
            else:
                break
            sim += 1

        if (self.root.heuristic < child.heuristic):
            child.wins += 1
        return child

    def backpropagation(self, node):
        """Function to propagate the score from the leafs to the tree root."""
        # print("-------- Backpropagation --------")
        while(node.parent is not None):
            parent = node.parent
            parent.plays += 1
            parent.wins += node.wins
            node = parent
        return node

    def MCTS_sample(self):
        """Most important function of MCTS. It triggers the process of selection, simulation and backpropagation."""
        node = self.selection()
        elapsed = time.time() - self.time_start
        print("    Time elapsed = " + str(elapsed))

        node = self.simulation(node)
        elapsed = time.time() - self.time_start
        print("    Time elapsed = " + str(elapsed))

        root = self.backpropagation(node)
        elapsed = time.time() - self.time_start
        print("    Time elapsed = " + str(elapsed))

        return root


    def run(self):
        """Monte Carlo Tree Search"""
        print("\n\n************  MCTS ************")
        self.time_start = time.time()
        elapsed = 0
        self.root.getFutureStates()
        itr = 0
        while(itr < self.max_iter) and (elapsed < self.max_time):
            print("##### Iteration " + str(itr) + " #####")
            self.root = self.MCTS_sample()
            itr += 1

        best_state = self.UCB_sample(self.root)
        print("    Number of nodes explored near root = " + str(len(self.root.visited_states)))
        print("    Best future state:")
        print(best_state)
        print("    Best action to take = " + str(best_state.action))

        return best_state




