import sys
import pygame
from pygame.locals import *
from tetris.image import Gallery
from tetris.util import Point, Dimension
from tetris.sound import Mixer
from tetris.piece import random_piece

# Size of the grid matrix.
GridSize = Dimension(10, 20)

class Tetris(object):

    def __init__(self):
        self.grid = []
        self.mixer = Mixer()
        self.stats = Statistics()
        self.curr_piece = random_piece()
        self.next_piece = random_piece()
        self.fall_speed = 30
        self.time_to_drop = self.fall_speed
        self.running = False

    def process_key_events(self, keys):

        if K_LEFT in keys:
            self.lateral_piece_move(-1)
        elif K_RIGHT in keys:
            self.lateral_piece_move(1)
        elif K_DOWN in keys:
            self.drop_piece()
        elif K_UP in keys:
            self.rotate_piece(1)
            
    def update(self):
        
        # Countdown to current piece drop
        self.time_to_drop -= 1
        if self.time_to_drop < 0:
            self.time_to_drop = self.fall_speed
            self.drop_piece(1)
        
    def render(self, gfx, gallery):
        
        gfx.blit(gallery.background, (0, 0))
        self.stats.render(gfx)
        
        # Render grid blocks
        for x in xrange(GridSize.width):
            for y in xrange(GridSize.height):
                if self.grid[x][y] > 0:
                    gallery.render_block(gfx, self.stats.level, self.grid[x][y] - 1, Point(x, y))
                elif self.grid[x][y] < 0:
                    gallery.render_ghost(gfx, (self.grid[x][y] * -1) - 1, Point(x, y))

        # Render next blocks
        for y in xrange(len(self.next_piece.grid)):
            for x in xrange(len(self.next_piece.grid[y])):
                if self.next_piece.grid[y][x]:
                    pt = Point(x - self.next_piece.origin.x, y - self.next_piece.origin.y)
                    gallery.render_next(gfx, self.stats.level, self.next_piece.grid[y][x] - 1, self.next_piece.size, pt)

    # Translate piece by delta
    def lateral_piece_move(self, dx):
        
        self.clear_grid_piece(self.curr_piece)
        self.curr_piece.pos.x += dx
        if not self.valid_move(self.curr_piece):
            self.curr_piece.pos.x -= dx
        else:
            self.mixer.lateral.play()
        self.set_grid_piece(self.curr_piece)
    
    # Rotate piece by delta
    def rotate_piece(self, dr):
        
        self.clear_grid_piece(self.curr_piece)
        
        if dr < 0:
            self.curr_piece.rotate_left()
            if not self.valid_move(self.curr_piece):
                self.curr_piece.rotate_right()
            else:
                self.mixer.rotate.play()
        elif dr > 0:
            self.curr_piece.rotate_right()
            if not self.valid_move(self.curr_piece):
                self.curr_piece.rotate_left()
            else:
                self.mixer.rotate.play()
                
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
                self.end_game()
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
            
        # Update statistics.
        self.mixer.play_dropped(len(cleared))
        if self.stats.update(len(cleared)):
            self.mixer.level_up.play()
            self.update_speed()
            
        self.new_piece()        
    
    def update_speed(self):
        if self.fall_speed >= 2:
            if self.fall_speed < 5:
                self.fall_speed -= 1
            elif self.fall_speed < 10:
                self.fall_speed -= 2
            else:
                self.fall_speed -= 3
            
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
            self.end_game()
        self.set_grid_piece(self.curr_piece)
    
    def new_game(self):
        self.grid = [[0 for y in xrange(GridSize.height)] for x in xrange(GridSize.width)]
        self.stats = Statistics()
        self.new_piece()
        self.mixer.start.play()
        self.mixer.loop_music()
        self.fall_speed = 30
        self.time_to_drop = self.fall_speed
        self.running = True
        
    def end_game(self):
        self.mixer.game_over.play()
        self.running = False
        
    def game_over(self):
        return not self.running

class Statistics(object):
    
    Scores = {
        0: 10, 
        1: 100, 
        2: 300, 
        3: 500, 
        4: 1000
    }
    
    def __init__(self):
        self.score = 0
        self.level = 0
        self.lines = 0
        
    # Render statistics values
    def render(self, gfx):

        font = pygame.font.SysFont("OCR A Extended", 14, True)
        label = font.render("LEVEL", 1, (255, 255, 255))
        gfx.blit(label, (70 - (label.get_width() / 2), 190))
        label = font.render("LINES", 1, (255, 255, 255))
        gfx.blit(label, (70 - (label.get_width() / 2), 260))
        
        font = pygame.font.SysFont("OCR A Extended", 28)
        label = font.render(repr(self.score), 1, (255, 255, 255))
        gfx.blit(label, (340 - label.get_width(), 5))
        label = font.render(repr(self.level), 1, (255, 255, 255))
        gfx.blit(label, (70 - (label.get_width() / 2), 207))
        label = font.render(repr(self.lines), 1, (255, 255, 255))
        gfx.blit(label, (70 - (label.get_width() / 2), 277))

    # Update stats based on # cleared lines
    def update(self, cleared):
        self.score += self.Scores[cleared]
        self.lines += cleared
        if self.lines / 10 > self.level:
            self.level += 1
            return True
        else:
            return False
