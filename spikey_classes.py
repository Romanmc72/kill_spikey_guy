import pygame as pg
from pygame.locals import *
import sys
import math as m
#import time as tm

class game:
    def __init__(self, background, play=True, characters=[]):
        pg.init()
        
    def add_character(self, character):
        self.characters.append(character)
        
    def update_characters(self):
        for character in self.characters:
            character._update()
            
    def __end__(self):
        pg.quit()
        print('Game Over')
        sys.exit()

class character:
    """
    This class defines a character in the game.
    It is the sub class that will be inherited
    from the player and enemy classes
    """
    
    
    def __init__(self,
                 x,
                 y,
                 image,
                 lives = 3,
                 speed = 1,
                 scale = 1,
                 appear = True
                 vector = 0):
        self.x = x
        self.y = y
        self.lives = lives
        self.speed = speed
        self.scale = scale
        self.image = pg.image.load(image)
        self.appear = appear
        self.vector = vector
        
        
    def _move(self, x_move, y_move):
        self.x += x_move*self.speed
        self.y += y_move*self.speed
        
    def _get_hurt(self, damage):
        self.lives -= damage
    
    def _update(self):
        

class player(character):
    """
    This class defines the player of the game
    it inherits the character class
    """
    def __init__(self,
                 lives,
                 speed,
                 scale,
                 image,
                 appear,
                 x = 300,
                 y = 300,
                 weapon = 0,
                 vector = 0):
        character__init__(self, x, y, lives, speed, scale, image, appear, vector)
        self.w = self.image.get_width()
        self.h = self.image.get_height()
        self.weapon = weapon
    
    
    def _rotation_degrees(self):
        x1, y1 = pg.mouse.get_pos()
        x2 = self.x + (self.w/2)
        y2 = self.y + (self.h/2)
        self.vector = m.atan2(y1-y2,x1-x2)
    
    
    
    
        