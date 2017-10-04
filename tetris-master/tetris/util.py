ScreenSize = (480, 450)

class Point(object):
    
    def __init__(self, x=0, y=0):
        self.x = x
        self.y = y

    def set(self, x, y):
        self.x = x
        self.y = y
        
    def translate(self, dx, dy):
        self.x += dx
        self.y += dy
        
    def tuple(self):
        return (self.x, self.y)
        
class Dimension(object):
    
    def __init__(self, width, height):
        self.width = width
        self.height = height
        
    def set(self, width, height):
        self.width = width
        self.height = height
    
    def rotate(self):
        return Dimension(self.height, self.width)
        
    def tuple(self):
        return (self.width, self.height)
