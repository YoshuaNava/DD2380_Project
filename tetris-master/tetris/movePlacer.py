
def place(self):
    actions = self.best_action
    rot = self.curr_piece.rotState.r
    tran = self.curr_piece.tranState.t

    if (actions[0] == rot and actions[1] == tran):
        self.drop_piece()

    while (actions[0] != rot):
        if(actions[0] > rot):
            self.rotate_piece(-1)
        elif (actions[0] < rot):
            self.rotate_piece(1)
    while actions[1] != tran:
        if (actions[1] > tran):
            self.lateral_piece_move(1)
        elif (actions[1] < tran):
            self.lateral_piece_move(-1)

class rotState(object):
    def __init__(self, r=0):
        self.r = r

    def set(self, r):
        self.r = r
        # self.rInBounds()
        
    def rot(self, dr):
        self.r += dr
        # self.rInBounds()

    def rInBounds(self):
        if (self.r > 3):
            self.r = self.r % 3
        elif(self.r < 0):
            tmp = (abs(self.r) // 4) +1
            self.r = self.r + 4*tmp

class tranState(object):
    def __init__(self, t=0):
        self.t = t

    def set(self, t):
        self.t = t
        
    def move(self, dt):
        self.t += dt