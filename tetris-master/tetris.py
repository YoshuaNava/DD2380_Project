import os
import sys
import pygame
from tetris.core import Core
from tetris.util import ScreenSize

os.environ['SDL_VIDEO_CENTERED'] = '1'
pygame.mixer.pre_init(44100, -16, 2, 4096)
pygame.init()
gfx = pygame.display.set_mode(ScreenSize)
pygame.display.set_caption('Tetris')

if __name__ == '__main__':
    Core(gfx).run()
