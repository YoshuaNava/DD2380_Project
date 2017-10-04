import random
from tetris.util import Point, Dimension

def random_piece():
    pieces = [SquarePiece, IPiece, JPiece, LPiece, TPiece, SPiece, ZPiece]
    return random.choice(pieces)()

# A 4x4 matrix representing a grid piece
class Piece(object):

    def __init__(self, x, y, width, height):
        self.grid = []
        self.pos = Point(x, y)
        self.origin = Point(0, 0)
        self.size = Dimension(width, height)
    
    # Set the grid values.
    def set(self, grid):
        self.grid = grid
        self.origin = Point(self.left(), self.top())

    # Rotate piece grid counter clockwise
    def rotate_left(self):
        rotated = zip(*self.grid)[::-1]
        self.set(rotated)
        self.size = self.size.rotate()
        
    # Rotate piece grid clockwise
    def rotate_right(self):
        rotated = zip(*self.grid[::-1])
        self.set(rotated)
        self.size = self.size.rotate()

    # Return the first non-empty row
    def top(self):
        for y in xrange(len(self.grid)):
            if len([x for x in xrange(len(self.grid[y])) if self.grid[y][x]]):
                return y
        return 0
    
    # Return the first non-empty column
    def left(self):
        left = 5
        for y in xrange(len(self.grid)):
            for x in xrange(len(self.grid[y])):
                if self.grid[y][x] and x < left:
                    left = x
        return left

class SquarePiece(Piece):
    def __init__(self):
        Piece.__init__(self, 3, -1, 2, 2)
        self.set([[0, 0, 0, 0],
                  [0, 1, 1, 0],
                  [0, 1, 1, 0],
                  [0, 0, 0, 0]])

class IPiece(Piece):
    def __init__(self):
        Piece.__init__(self, 3, -2, 4, 1)
        self.set([[0, 0, 0, 0],
                  [0, 0, 0, 0],
                  [1, 1, 1, 1],
                  [0, 0, 0, 0],
                  [0, 0, 0, 0]])
    
class JPiece(Piece):
    def __init__(self):
        Piece.__init__(self, 3, -1, 3, 2)
        self.set([[0, 0, 0, 0],
                  [2, 2, 2, 0],
                  [0, 0, 2, 0],
                  [0, 0, 0, 0]])
        
class LPiece(Piece):
    def __init__(self):
        Piece.__init__(self, 2, -1, 3, 2)
        self.set([[0, 0, 0, 0],
                  [0, 2, 2, 2],
                  [0, 2, 0, 0],
                  [0 ,0, 0, 0]])
        
class TPiece(Piece):
    def __init__(self):
        Piece.__init__(self, 2, -2, 3, 2)
        self.set([[0, 0, 0, 0, 0],
                  [0, 0, 0, 0, 0],
                  [0, 1, 1, 1, 0],
                  [0, 0, 1, 0, 0],
                  [0, 0, 0, 0, 0]])
        
class SPiece(Piece):
    def __init__(self):
        Piece.__init__(self, 2, -1, 3, 2)
        self.set([[0, 0, 0, 0, 0],
                  [0, 0, 3, 3, 0],
                  [0, 3, 3, 0, 0],
                  [0, 0, 0, 0, 0]])
                
class ZPiece(Piece):
    def __init__(self):
        Piece.__init__(self, 2, -1, 3, 2)
        self.set([[0, 0, 0, 0, 0],
                  [0, 3, 3, 0, 0],
                  [0, 0, 3, 3, 0],
                  [0, 0, 0, 0, 0]])
