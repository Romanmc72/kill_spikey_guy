import pygame as pg
from pygame.locals import *
import sys
import math as m
import functions as fn
# import time as tm


class Game:
    def __init__(self, background: str, done: bool = False, characters: object = []) -> None:
        pg.init()
        self.background = pg.image.load(background)
        self.done = done
        self.characters = characters
        self.h = self.background.get_height()
        self.w = self.background.get_width()
        
    def add_character(self, character):
        self.characters.append(character)
        
    def update_characters(self):
        for character in self.characters:
            character.update()

    def play(self):
        while not self.done:
            for event in pg.event.get():



            update_characters()

        self.__end__()

    def __end__(self):
        pg.quit()
        print('Game Over')
        sys.exit()


class Character:
    """
    This class defines a character in the game.
    It is the sub class that will be inherited
    from the player and enemy classes
    """
    def __init__(self,
                 x: float,
                 y: float,
                 lives: int,
                 speed: int,
                 scale: float,
                 image: str,
                 appear: bool,
                 angle: float) -> None:
        self.x = x
        self.y = y
        self.lives = lives
        self.speed = speed
        self.scale = scale
        self.image = pg.image.load(image)
        self.appear = appear
        self.angle = angle
        self.rotated_image = None

    def _move(self, x_move, y_move):
        self.x += x_move*self.speed
        self.y += y_move*self.speed

    def update(self, screen):
        if self.appear:
            if self.angle != 0:
                self.rotated_image = pg.transform.rotate(self.image, self.angle)
                offset_x, offset_y = fn.get_offset(self.image, self.rotated_image)
                screen.blit(self.rotated_image, (self.x + offset_x, self.y + offset_y))
            else:
                screen.blit(self.image, (self.x, self.y))

    def get_hurt(self, damage):
        self.lives -= damage


class Player(Character):
    """
    This class defines the player of the game
    it inherits the character class
    """
    def __init__(self,
                 speed: int,
                 scale: float,
                 image: str,
                 appear: bool,
                 x: float = 300.0,
                 y: float = 300.0,
                 lives: int = 3,
                 weapons: list = None,
                 angle: float = 0,
                 rotated_image: pg.image = None) -> None:
        Character.__init__(self, x, y, lives, speed, scale, image, appear, angle, rotated_image)
        self.w = self.image.get_width()
        self.h = self.image.get_height()
        self.weapons = weapons
    
    def _rotation_degrees(self):
        x1, y1 = pg.mouse.get_pos()
        x2 = self.x + (self.w/2)
        y2 = self.y + (self.h/2)
        self.angle = m.atan2(y1-y2,x1-x2)
