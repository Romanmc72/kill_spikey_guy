import pygame as pg
import sys
import numpy.random as r
# import math as m
import functions as fn
# from pygame.locals import *
# import time as tm

#TODO add barriers and obstacles

class Game:
    def __init__(self, background: str, done: bool = False, characters: list = []) -> None:
        pg.init()
        self.background = pg.image.load(background)
        self.done = done
        self.characters = characters
        self.players = []
        self.enemies = []
        self.h = self.background.get_height()
        self.w = self.background.get_width()
        self.screen = pg.display.set_mode((self.w, self.h))
        self.key_state = {'left': 0,
                          'right': 0,
                          'up': 0,
                          'down': 0}
        
    def add_character(self, character):
        if character.is_player:
            self.players.append(character)
        elif character.is_enemy:
            self.enemies.append(character)
        else:
            print("ERROR: character of unknown type added to game")
            pg.quit()
            sys.exit(4)
        self.characters.append(character)

    def remove_character(self, character):
        self.characters.pop(self.characters.index(character))
        
    def update_characters(self, keys):
        for character in self.characters:
            if character in self.players
                character.update(self.screen, keys,)

    def play(self):
        while not self.done:
            for event in pg.event.get():
                self.get_keys(event=event)
                if event.type == pg.QUIT:
                    self.done = True
                elif event.type == pg.KEYDOWN:
                    if event.key == pg.K_ESCAPE:
                        self.done = True

            self.screen.blit(self.background, (0, 0))
            self.update_characters(self.key_state)
            pg.display.flip()

        self.__end__()

    def get_keys(self, event):
        if event.type == pg.KEYDOWN:
            if event.key == pg.K_d:
                self.key_state['right'] = True
            elif event.key == pg.K_a:
                self.key_state['left'] = True
            elif event.key == pg.K_w:
                self.key_state['up'] = True
            elif event.key == pg.K_s:
                self.key_state['down'] = True
            elif event.key == pg.K_SPACE:
                self.key_state['space'] = True
        elif event.type == pg.KEYUP:
            if event.key == pg.K_d:
                self.key_state['right'] = False
            elif event.key == pg.K_a:
                self.key_state['left'] = False
            elif event.key == pg.K_w:
                self.key_state['up'] = False
            elif event.key == pg.K_s:
                self.key_state['down'] = False
            elif event.key == pg.K_SPACE:
                self.key_state['space'] = False

    def __end__(self):
        pg.quit()
        print('Game Over')
        sys.exit()

class Boundaries:
    def __init__(self, x, y, w, h):
        self.left = x
        self.right = x + w
        self.top = y
        self.bottom = y + h
        self.top_left     = (x    , y    ),
        self.top_right    = (x + w, y    ),
        self.bottom_left  = (x    , y + h),
        self.bottom_right = (x + w, y + h)
        self.bounds = [self.top_left,
                       self.top_right,
                       self.bottom_left,
                       self.bottom_right]


class _Character:
    """
    This class defines a character in the game.
    It is the parent class that will be inherited
    from the player and enemy classes, do not change
    or use this class
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
        self.rotated_image = pg.image.load(image)
        self.w = self.image.get_width()
        self.h = self.image.get_height()
        self.bounds = Boundaries(x=self.x,
                                 y=self.y,
                                 w=self.w,
                                 h=self.h)

    def is_alive(self):
        if self.lives > 0:
            self.appear = True
            return True
        else:
            self.appear = False
            return False

    def _re_bound(self):
        self.bounds = Boundaries(x=self.x,
                                 y=self.y,
                                 w=self.w,
                                 h=self.h)

    def _move(self, x_move, y_move):
        self.x += x_move*self.speed
        self.y += y_move*self.speed

    def get_hurt(self, damage):
        self.lives -= damage

    def is_touching(self, other):
        return fn.is_touching(self.bounds, other.bounds)

class Player(_Character):
    """
    This class defines the player of the game
    it inherits the character class
    """
    def __init__(self,
                 image: str,
                 speed: int = 2,
                 scale: float = 1.0,
                 appear: bool = True,
                 x: float = 300.0,
                 y: float = 300.0,
                 lives: int = 3,
                 weapons: list = None,
                 angle: float = 0) -> None:
        _Character.__init__(self, x, y, lives, speed, scale, image, appear, angle)
        self.weapons = weapons
        self.is_player = True
        self.is_enemy = False
    
    def _rotation_degrees(self):
        center = (self.x + self.w / 2, self.y + self.h / 2)
        self.angle = fn.get_angle(center, pg.mouse.get_pos())

    def _get_movement(self, keys):
        if keys['left']:
            self._move(-1, 0)
        if keys['right']:
            self._move(1, 0)
        if keys['up']:
            self._move(0, -1)
        if keys['down']:
            self._move(0, 1)

    def update(self, screen, keys, enemy):
        if self.appear:
            if self.is_touching(enemy):
                self.get_hurt(1)
            self.is_alive()
            self._get_movement(keys)
            self._rotation_degrees()
            self.rotated_image = pg.transform.rotate(self.image, self.angle)
            offset_x, offset_y = fn.get_offset(self.image, self.rotated_image)
            screen.blit(self.rotated_image, (self.x + offset_x, self.y + offset_y))

    def extra_life(self, life):
        self.lives += life


class Enemy(_Character):
    def __init__(self,
                 image,
                 x = 0,
                 y = 0,
                 lives = 1,
                 speed = 2,
                 scale = 1,
                 appear = True,
                 angle = 0):
        _Character.__init__(self, x, y, lives, speed, scale, image, appear, angle)
        self.is_player = False
        self.is_enemy = True

    def follow(self, other):
        if other.is_player():
            if self.x < other.x:
                self._move(1, 0)
            elif self.x > other.x:
                self._move(-1, 0)
            if self.y < other.y:
                self._move(0, 1)
            elif self.y > other.y:
                self._move(0, -1)

    # def is_hit(self, obj):
    #     if

    def update(self, screen, other): #, vector):
        if self.appear:
            self.follow(other)
            screen.blit(self.image, (self.x, self.y))

