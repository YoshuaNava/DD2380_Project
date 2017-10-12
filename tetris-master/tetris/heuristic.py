from tetris.util import Dimension
GridSize = Dimension(10, 20)

def heuristic(gamefield):
    # Heuristic functions
    h1 = getNumHoles(gamefield)          # Minimize this value (i.e. negative factor)
    h2 = getAggregateHeight(gamefield) # Minimize
    h3 = getHeightVariance(gamefield)  # Minimize
    h4 = getClearedLines(gamefield)    # Maximize
    # print("Holes " + str(h1))
    # print("AggHeight " + str(h2))
    # print("HeightVar " + str(h3))
    # print("Cleared lines " + str(h4))

    # Factors for respectively function
    a = -0.5
    b = -0.4
    c = -0.2
    d = 2.0

    # Heuristic
    h = a * h1 + b * h2 + c * h3 + d * h4
    return h


def getClearedLines(gamefield):
    # Find cleared rows
    num_cleared = 0
    for row in xrange(GridSize.height):
        if (len([col for col in xrange(GridSize.width) if gamefield[row][col]]) == GridSize.width):
            num_cleared += 1
            print("CCCCCCCCCCCCCCCCLLLLLLLLLLLLLLLLLLLEEEEEEEEEEEEEEEEEEAAAAAAAAAAAAAAAAAAARRRRRRRRRRRRRRREEEEEEEEEEEEEEEEEEDDDDDDDDDD")
            print(num_cleared)

    return num_cleared


# Number of holes
def getNumHoles(gamefield):
    nHoles = 0
    maxheights = getMaxHeights(gamefield)

    for row in xrange(4,GridSize.height):
        for col in xrange(GridSize.width):
            if(gamefield[row][col] <= 0):
                if(GridSize.height - 1 - row < maxheights[col]):
                    nHoles += 1
    return nHoles


# Number of aggregate height
def getAggregateHeight(gamefield):
    sumHeight = sum(getMaxHeights(gamefield))
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
def getMaxHeights(gamefield):
    heights = []
    for col in xrange(GridSize.width):
        tempHeight = []
        for row in xrange(4,GridSize.height):
            if (gamefield[row][col] > 0):
                tempHeight.append(GridSize.height - 1 - row)
        if tempHeight:
            heights.append(max(tempHeight))
        else:
            heights.append(0)
    return heights
