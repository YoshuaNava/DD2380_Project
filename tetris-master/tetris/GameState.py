import copy
from tetris.util import Point, Dimension
from tetris.piece import random_piece
GridSize = Dimension(10, 20)

class GameNode():
    def __init__(self, grid, piece, nextpiece):
        self.hashtable = [0] * 1000000 # hashtable to avoid duplicate children
        self.children = [] # hold every child state
        self.grid = copy.deepcopy(grid)
        self.curr_piece = copy.deepcopy(piece)
        self.next_piece = copy.deepcopy(nextpiece)

    def findChildren(self):
        for translation in range(-5,6,1): # translations relative middle
            for rotation in range(0, 4, 1): # number of rotations
                grid = copy.deepcopy(self.grid)
                piece = copy.deepcopy(self.curr_piece)
                nextPiece = copy.deepcopy(self.next_piece)

                # get the new state (for each performed move)
                newState = TetrisGame(grid, piece, nextPiece, translation, rotation)
                # get a state string (in order to hash it)
                newStateGrid = newState.getGrid()
                newStateString = self.gridToString(newStateGrid)
                # calculate the hash value
                hashVal = abs(hash(newStateString))

                # check for hash collision
                if (self.hashtable[hashVal % 1000000] == 0):
                    self.hashtable[hashVal % 1000000] = 1
                    self.children.append(newState)
                    self.printGrid(newState.getGrid())

    def printGrid(self, grid):
        print "\n"
        state = [[0 for i in xrange(GridSize.width)] for i in xrange(GridSize.height)]
        for x in xrange(GridSize.width):
            for y in xrange(GridSize.height):
                state[y][x] = grid[x][y]
        for row in state:
            print row

    def getGrid(self):
        return self.grid

    def gridToString(self, grid):
        stateString = ""
        for x in xrange(GridSize.width):
            for y in xrange(GridSize.height):
                stateString += str(grid[x][y])
        return stateString

    def getNextStates(self):
        self.findChildren()
        return self.children

class TetrisGame():
    def __init__(self, grid, piece, nextPiece, translation, rotation):
        self.grid = copy.deepcopy(grid)
        self.curr_piece = copy.deepcopy(piece)
        self.next_piece = copy.deepcopy(nextPiece)

        # perform action
        self.rotate_piece(rotation)
        self.lateral_piece_move(translation)
        self.drop_piece()

    def getGrid(self):
        return self.grid

    def getPiece(self):
        return self.curr_piece

    def getNextPiece(self):
        return self.next_piece

    # Translate piece by delta
    def lateral_piece_move(self, dx):
        self.clear_grid_piece(self.curr_piece)
        self.curr_piece.pos.x += dx
        if not self.valid_move(self.curr_piece):
            self.curr_piece.pos.x -= dx

        self.set_grid_piece(self.curr_piece)

    # Rotate piece by delta
    def rotate_piece(self, dr):

        self.clear_grid_piece(self.curr_piece)

        if dr < 0:
            self.curr_piece.rotate_left()
            if not self.valid_move(self.curr_piece):
                self.curr_piece.rotate_right()
        elif dr > 0:
            # EXTENT ROTATION FUNCTION
            for _ in range(dr):
                self.curr_piece.rotate_right()
                if not self.valid_move(self.curr_piece):
                    self.curr_piece.rotate_left()

        self.set_grid_piece(self.curr_piece)

    # Drop piece to the bottom
    def drop_piece(self, incr=GridSize.height):

        self.clear_grid_piece(self.curr_piece)

        # Find grid bottom
        place = False
        for i in range(incr):
            self.curr_piece.pos.y += 1
            if not self.valid_move(self.curr_piece):
                self.curr_piece.pos.y -= 1
                place = True
                break

        self.set_grid_piece(self.curr_piece)
        if place:
            if self.curr_piece.pos.y + self.curr_piece.origin.x <= 0:
                print "END GAME!"
            else:
                self.place_piece(self.curr_piece)

    # Place piece at grid bottom
    def place_piece(self, piece):

        # Find cleared rows
        cleared = []
        for y in xrange(GridSize.height):
            if (len([x for x in xrange(GridSize.width) if self.grid[x][y]]) == GridSize.width):
                cleared.append(y)

        # Clear rows & shift down remains.
        if cleared:
            for row in cleared:
                for x in xrange(GridSize.width):
                    self.grid[x][row] = 0
            for row in cleared:
                self.shift_row_down(row)

        self.new_piece()

    # Shift above rows down from cleared row.
    def shift_row_down(self, row):
        for x in xrange(GridSize.width):
            for y in reversed(xrange(row)):
                self.grid[x][y + 1] = self.grid[x][y]
                self.grid[x][y] = 0

    # Set piece values into grid.
    def set_grid_piece(self, piece):

        # Find and set piece ghost grid points
        yorig = piece.pos.y
        for y in xrange(GridSize.height - piece.pos.y):
            piece.pos.y += 1
            if not self.valid_move(piece):
                piece.pos.y -= 1
                break

        for y in xrange(len(piece.grid)):
            for x in xrange(len(piece.grid[y])):
                if piece.grid[y][x]:
                    self.grid[piece.pos.x + x][piece.pos.y + y] = (piece.grid[y][x] * -1)

        # Set grid values for piece.
        piece.pos.y = yorig
        for y in xrange(len(piece.grid)):
            for x in xrange(len(piece.grid[y])):
                if piece.grid[y][x] and piece.pos.y + y >= 0:
                    self.grid[piece.pos.x + x][piece.pos.y + y] = piece.grid[y][x]

    # Remove piece values from grid.
    def clear_grid_piece(self, piece):

        # Clear ghost grid points.
        for x in xrange(GridSize.width):
            for y in xrange(GridSize.height):
                if self.grid[x][y] < 0:
                    self.grid[x][y] = 0

        # Clear piece grid points.
        for y in xrange(len(piece.grid)):
            for x in xrange(len(piece.grid[y])):
                if piece.grid[y][x] and piece.pos.y + y >= 0:
                    self.grid[piece.pos.x + x][piece.pos.y + y] = 0

    # Check if piece can be moved to new location
    def valid_move(self, piece):

        for y in xrange(len(piece.grid)):
            for x in xrange(len(piece.grid[y])):

                pt = Point(piece.pos.x + x, piece.pos.y + y)
                if piece.grid[y][x] and pt.y >= 0:
                    if pt.x < 0 or pt.x >= GridSize.width or pt.y >= GridSize.height:
                        return False
                    if self.grid[pt.x][pt.y]:
                        return False
        return True

    def new_piece(self):
        self.curr_piece = self.next_piece
        self.next_piece = random_piece()
        if not self.valid_move(self.curr_piece):
            print "END GAME!"
        self.set_grid_piece(self.curr_piece)



