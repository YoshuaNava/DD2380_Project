import random, time, util, sys, math



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
        self.maxLength = 10  # max search length
        self.maxIter = 20
        self.maxTime = 1.0
        self.maxActions = 200
        self.time_start = 0
        self.root = Node(gameState)
        self.root.parent = None
        self.root.children = []
        self.root.plays = 1
        self.C = 1.4


    def UCB(self, node, child, C):
        return child.wins + self.C * math.sqrt( math.log(node.plays) / child.plays )


    def UCB_sample(self, node):
        ##print("-------- UCB sampling --------")
        weights = np.zeros(len(node.children))
        i = 0
        for child in node.children:
            w = UCB(self, node, child)
            weights[i] = w
            i += 1
            '''#print("Child", child)
            #print("Child parent", child.parent)
            #print("Child plays", child.plays)
            #print("Child wins", child.wins)
            #print("Child action", child.action)
            #print("Child children", len(child.children))'''

        sum_weights = np.sum(weights)
        if(sum_weights != 0):
            weights /= sum_weights
            i = 0
            for child in node.children:
                child.UCB = weights[i]
                i += 1
        idx_max = np.argmax(weights)
        '''
        #print("weights", weights)
        #print("idx_max", idx_max)
        '''

        return node.children[idx_max]


    def expansion(self, state, node):
    #    #print("-------- Expansion --------")
        actionsTaken = [child.action for child in node.children]
        legalActions = state.getLegalActions(node.state)
        actionsLeft = [action for action in legalActions if action not in actionsTaken]

        if(len(actionsLeft)==0):
            return node, random.choice(node.children)
        randAction = random.choice(actionsLeft)
        '''
        #print("Actions taken until now", actionsTaken)
        #print("Legal actions", legalActions)
        #print("Actions left to take", actionsLeft)
        #print("Random action", randAction)
        '''

        nextState = node.state.generateSuccessor(randAction)
        child = Node(nextState)
        child.parent = node
        child.action = randAction
        child.children = []
        node.children.append(child)

        return node, child



    def selection(self, state, root, maxLength):
    #    #print("-------- Selection --------")
        node = root
        legalActions = state.getLegalActions(node.state)
        expanded = False

        treeDepth = 0

        if(len(node.children) < len(legalActions)):
            _, node = expansion(state, node)
        else:
            while(len(node.children) > 0):
                legalActions = state.getLegalActions(node.state)
                if(len(node.children) == len(legalActions)):
                    node = UCB_sample(state, node)
                else:
                    _, node = expansion(state, node)
                    expanded = True

                treeDepth+=1
    #            #print("Tree depth", treeDepth)
            if (expanded == False):
                _, node = expansion(state, node)

        node.plays += 1

        return node



    def simulation(self, child, maxLength):
    #    #print("-------- Simulation --------")
        state = child.state
        points = 0
        itr = 1

        elapsed = time.time() - self.time_start
        while (itr <= maxLength and elapsed < 0.8):
            legalActions = state.getLegalActions(state)
            action = random.choice(legalActions)
            points = points + state.getPoints(child.state, state, self.root.state)
            state = state.generateSuccessor(action)
            itr += 1
            elapsed = time.time()-self.time_start
        if(points > 0):
            child.wins += 1


        return child





    def backpropagation(self, child):
    #    #print("-------- Backpropagation --------")
        node = child
        while(node.parent is not None):
            parent = node.parent
            parent.plays += 1
            parent.wins += node.wins
            node = parent

        return node



    def MCTS_sample(self, root, maxLength):
        node = selection(state, root, maxLength)
        node = simulation(self, node, maxLength)
        root = backpropagation(node)
        return root




mcts = None

def play(self, gameState):
    """Monte Carlo Tree Search"""
    print("\n*********  MCTS *********")

    if(gameState.getRound() == 0):
        mcts = MonteCarloTreeSearch(gameState)

 	mcts.time_start = time.time()
    elapsed = 0
    actions = gameState.getLegalActions()
    bestAction = random.choice(actions)

    if (mcts.root.state != gameState):
        mcts.root = Node(gameState)
        mcts.root.parent = None
        mcts.root.children = []
        mcts.root.plays = 1

    t = 0
    while(t < mcts.maxIter and elapsed < mcts.maxTime):
        mcts.root = MCTS_sample()
        t+=1
        elapsed = time.time() - mcts.time_start

    next_node = UCB_sample()
    bestAction = next_node.action

    return bestAction



