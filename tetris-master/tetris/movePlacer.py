
def place(self, column, rotation):
    print self.curr_piece.rotState.r
    if (self.curr_piece.pos.x > column):
        self.lateral_piece_move(-1)
    elif (self.curr_piece.pos.x < column):
        self.lateral_piece_move(1)

    if (self.curr_piece.rotState.r > rotation):
    	self.rotate_piece(1)
    elif (self.curr_piece.rotState.r < rotation):
    	self.rotate_piece(-1)
    
    if (self.curr_piece.pos.x == column) and (self.curr_piece.rotState.r == rotation):
    	self.drop_piece()


class rotState(object):
    def __init__(self, r=0):
        self.r = r

    def set(self, r):
        self.r = r
        
    def rot(self, dr):
        self.r += dr