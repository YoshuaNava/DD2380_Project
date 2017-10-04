import os
import pygame
from tetris.util import Point, Dimension

# Image dimensions
BlockSize = Dimension(20, 20)
BackgroundSize = Dimension(480, 450)
    
# Load an image from the file system
def load(filename):
    return pygame.image.load(os.path.join("images", filename)).convert()

class Gallery(object):
    
    def __init__(self):
        
        self.splash = load("splash.png")
        self.background = load("tetris-background.png")
        self.blocks = {}
        self.fading = {}
        
        # Parse blocks from sprite sheet
        width, height = BlockSize.width, BlockSize.height
        blocksheet = SpriteSheet("blocks.png")
        for level in xrange(11):
            blockset = []
            for index in xrange(3):
                sub = blocksheet.subimage(level * width, index * height, width, height)
                blockset.append(Block(sub))
            self.blocks[level] = blockset
            
        # Parse fading blocks from sprite sheet
        xoff = BlockSize.width * 11
        for index in xrange(3):
            blockset = []
            for fade in xrange(10):
                sub = blocksheet.subimage(fade * width + xoff, index * height, width, height)
                blockset.append(Block(sub))
            self.fading[index] = blockset

    # Render a block with level & index at specified grid point.
    def render_block(self, gfx, level, index, pt):
        level = level % 11
        if level in self.blocks and index >= 0 and index < 3:
            self.blocks[level][index].render(gfx, pt)

    # Render a next block with an index at specified grid point.
    def render_next(self, gfx, level, index, size, pt):
        level = level % 11
        if level in self.blocks and index >= 0 and index < 3:
            self.blocks[level][index].render_next(gfx, size, pt)

    # Render a fading block with an index and fade at specified grid point.
    def render_fading(self, gfx, index, fade, pt):
        if index in self.fading and fade >= 0 and fade <= 10:
            self.fading[index][fade].render(gfx, pt)

    # Render a ghost block with an index at specified grid point
    def render_ghost(self, gfx, index, pt):
        if index in self.fading:
            fade = 3 if index == 1 else 4
            self.fading[index][fade].render(gfx, pt)

class Block(object):
    
    def __init__(self, image):
        self.image = image

    # Render the block at specified grid [x,y] indices
    def render(self, gfx, pt):
        pos = self.grid_to_pos(pt)
        gfx.blit(self.image, pos.tuple())
        
    # Render the next block at specified grid [x,y] indices
    def render_next(self, gfx, size, pt):
        pos = self.next_to_pos(size, pt)
        gfx.blit(self.image, pos.tuple())
        
    # Convert grid point to its [x,y] position coordinates
    def grid_to_pos(self, pt):
        x = pt.x * BlockSize.width + 140
        y = pt.y * BlockSize.height + 40
        return Point(x, y)
    
    # Cconvert next grid point to its [x,y] position coordinates
    def next_to_pos(self, size, pt):
        center = Point((size.width * BlockSize.width) / 2, (size.height * BlockSize.height) / 2)
        offset = Point(411 - center.x, 84 - center.y)
        x = pt.x * BlockSize.width + offset.x
        y = pt.y * BlockSize.height + offset.y
        return Point(x, y)

class SpriteSheet(object):
    
    def __init__(self, filename):
        self.sheet = load(filename)
        
    # Get a subimage from the sheet.
    def subimage(self, x, y, width, height):
        rect = pygame.Rect(x, y, width, height)
        image = pygame.Surface(rect.size).convert()
        image.blit(self.sheet, (0, 0), rect)
        return image
