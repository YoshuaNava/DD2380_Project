import os
import pygame

def load(filename):
    return pygame.mixer.Sound(os.path.join('sounds', filename))

def load_music(filename):
    return pygame.mixer.music.load(os.path.join('sounds', filename))

class Sound(object):
    def __init__(self, filename):
        self.sound = load(filename)
    def play(self):
        self.sound.stop()
        self.sound.play(0)
    def stop(self):
        self.sound.stop()

class Mixer(object):
    
    def __init__(self):
        self.clear = Sound('clear.wav')
        self.drop = Sound('drop.wav')
        self.lateral = Sound('lateralmove.wav')
        self.level_up = Sound('levelup.wav')
        self.rotate = Sound('rotate.wav')
        self.select = Sound('select.wav')
        self.start = Sound('start.wav')
        self.tetris = Sound('tetris.wav')
        self.game_over = Sound('gameover.wav')
        self.music = load_music('tetrismusic.wav')

    def loop_music(self):
        pygame.mixer.music.play(-1, 0.0)

    def stop_music(self):
        pygame.mixer.music.stop()
                        
    def pause(self):
        pygame.mixer.pause()
        
    def unpause(self):
        pygame.mixer.unpause()
            
    def play_dropped(self, cleared):
        sounds = {
            4: self.tetris,
            3: self.clear,
            2: self.clear,
            1: self.clear,
            0: self.drop
        }
        sounds[cleared].play()
