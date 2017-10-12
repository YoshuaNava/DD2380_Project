from tetris.util import Dimension
GridSize = Dimension(10, 20)

def heuristic(gamefield):
    # Heuristic functions
    h1 = getNumHoles(gamefield)          # Minimize this value (i.e. negative factor)
    h2 = getAggregateHeight(gamefield) # Minimize
    #h3 = getHeightVariance(gamefield)  # Minimize
    #h4 = getClearedLines(gamefield)    # this exists implicit in h2

    # Factors for respectively function
    a = -1
    b = -0.5
    c = 0
    d = 0

    h3 = 0
    # Heuristic
    h = a * h1 + b * h2 + c * h3
    return h


def getClearedLines(gamefield):
    # Find cleared rows
    num_cleared = 0
    for row in xrange(GridSize.height):
        if (len([col for col in xrange(GridSize.width) if gamefield[row][col]]) == GridSize.width):
            num_cleared += 1

    return num_cleared


# Number of holes
def getNumHoles(gamefield):
    nHoles = 0
    maxheights = getMaxHeights(gamefield)

    for row in xrange(5,GridSize.height):
        for col in xrange(GridSize.width):
            if(gamefield[row][col] == 0):
                if(GridSize.height - 1 - row < maxheights[col]):
                    nHoles += 1

    return nHoles


# Number of aggregate height
def getAggregateHeight(gamefield):
    sumHeight = sum(getSquaredMaxHeights(gamefield))
    return sumHeight


# Variation of column heights
def getHeightVariance(gamefield):
    cols = getMaxHeights(gamefield)
    variance = 0
    for i in xrange(len(cols)):
        if (i < len(cols) - 1):
            variance += abs(cols[i] - cols[i + 1])
    return variance


# Get height of each column
def getSquaredMaxHeights(gamefield):
    heights = []
    for col in xrange(GridSize.width):
        tempHeight = []
        for row in xrange(5,GridSize.height):
            if (gamefield[row][col] > 0):
                tempHeight.append(GridSize.height - 1 - row)
        if len(tempHeight) > 0:
            heights.append(max(tempHeight)**2)
        else:
            heights.append(0)
    return heights


# Get height of each column
def getMaxHeights(gamefield):
    heights = []
    for col in xrange(GridSize.width):
        tempHeight = []
        for row in xrange(5,GridSize.height):
            if (gamefield[row][col] > 0):
                tempHeight.append(GridSize.height - row)
        if len(tempHeight) > 0:
            heights.append(max(tempHeight))
        else:
            heights.append(0)
    return heights
