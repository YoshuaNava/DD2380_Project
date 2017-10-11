from tetris.util import Dimension
GridSize = Dimension(10, 20)

def heuristic(gamefield):
    # Heuristic functions
    h1 = nHoles(gamefield)          # Minimize this value (i.e. negative factor)
    h2 = aggregateHeight(gamefield) # Minimize
    h3 = heightVariance(gamefield)  # Minimize

    # Factors for respectively function
    a = -0.5
    b = -0.4
    c = -0.2

    # Heuristic
    h = a * h1 + b * h2 + c * h3
    return h

# Number of holes
def nHoles(gamefield):
    nHoles = 0
    maxheights = getMaxHeights(gamefield)

    for row in xrange(4,GridSize.height):
        for col in xrange(GridSize.width):
            if(gamefield[row][col] <= 0):
                if(GridSize.height - 1 - row < maxheights[col]):
                    nHoles += 1
    return nHoles


# Number of aggregate height
def aggregateHeight(gamefield):
    sumHeight = sum(getMaxHeights(gamefield))
    return sumHeight

# Variation of column heights
def heightVariance(gamefield):
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
