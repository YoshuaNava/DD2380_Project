import copy
from tetris.util import Point, Dimension
from tetris.piece import random_piece
GridSize = Dimension(10, 20)

##### TetrisGame simulates a set of actions ######


class TetrisGame():
    Scores = {
        0: 10, 
        1: 100, 
        2: 300, 
        3: 500, 
        4: 1000
    }

    def __init__(self, grid, piece, nextPiece, rotation, translation, level=0, lines=0, score=0):
        self.grid = copy.deepcopy(grid)
        self.curr_piece = copy.deepcopy(piece)
        self.next_piece = copy.deepcopy(nextPiece)
        self.action = (copy.deepcopy(rotation), copy.deepcopy(translation))
        self.end_of_game = False
        self.cleared_rows = 0
        self.level = level
        self.lines = lines
        self.score = score

        # perform actions IF NOT ROOT NODE
        if (rotation != -1):
            self.rotate_piece(rotation)
            self.lateral_piece_move(translation)
            self.drop_piece()


    def updateScore(self):
        # Find cleared rows
        cleared = []
        for y in xrange(GridSize.height):
            if (len([x for x in xrange(GridSize.width) if self.grid[x][y]]) == GridSize.width):
                cleared.append(y)
        self.score += self.Scores[len(cleared)]
        self.lines += len(cleared)
        if self.lines / 10 > self.level:
            self.level += 1

    def getGrid(self):
        return self.grid

    def getPiece(self):
        return self.curr_piece

    def getNextPiece(self):
        return self.next_piece

    def getAction(self):
        return self.action

    # Translate piece by delta
    def lateral_piece_move(self, dx):
        for _ in range(abs(dx)):
            self.clear_grid_piece(self.curr_piece)
            self.curr_piece.pos.x += dx/abs(dx)
            if not self.valid_move(self.curr_piece):
                self.curr_piece.pos.x -= dx/abs(dx)

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
                print "End of game. No more valid placements for this piece"
                self.end_of_game = True
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
        self.cleared_rows += 1
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
                    self.grid[piece.pos.x + x][piece.pos.y +
                                               y] = (piece.grid[y][x] * -1)

        # Set grid values for piece.
        piece.pos.y = yorig
        for y in xrange(len(piece.grid)):
            for x in xrange(len(piece.grid[y])):
                if piece.grid[y][x] and piece.pos.y + y >= 0:
                    self.grid[piece.pos.x +
                              x][piece.pos.y + y] = piece.grid[y][x]

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
            self.end_of_game = True

        self.set_grid_piece(self.curr_piece)
