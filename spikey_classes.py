import pygame as pg
import functions as fn
import sys
import time
import math as m
# import numpy.random as r
# from pg.locals import *
# TODO add barriers and obstacles
# TODO make the fist kill the spikey guy


class Game:
    def __init__(self,
                 background: str,
                 done: bool = False,
                 characters: list = []) -> None:
        pg.init()
        self.background = pg.image.load(background)
        self.done = done
        self.characters = characters
        # self.players = []
        # self.enemies = []
        self.x = 0
        self.y = 0
        self.h = self.background.get_height()
        self.w = self.background.get_width()
        self.screen = pg.display.set_mode((self.w, self.h))
        self.key_state = {'left': 0,
                          'right': 0,
                          'up': 0,
                          'down': 0,
                          'space': False}
        self.bounds = Boundaries(x=self.x,
                                 y=self.y,
                                 w=self.w,
                                 h=self.h)
        
    def add_character(self, character):
        self.characters.append(character)
        character.add_to_screen(self)

    def remove_character(self, character):
        self.characters.pop(self.characters.index(character))
        
    def update_characters(self):
        enemies = [character for character in self.characters if character.is_enemy and character.appear]
        players = [character for character in self.characters if character.is_player and character.appear]
        for player in players:
            player.update(self.screen, self.key_state, enemies)
            for life in range(player.lives):
                self.screen.blit(pg.transform.scale(player.image, (20, 20)), (25 + 20 * life, 25))
        [enemy.update(self.screen, players) for enemy in enemies]
        if not players:
            self.done = True
        for player in players:
            if not player.alive:
                self.done = True

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
            self.update_characters()
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
        self.top = y + h
        self.bottom = y
        self.top_left = (x, y + h)
        self.top_right = (x + w, y + h)
        self.bottom_left = (x, y)
        self.bottom_right = (x + w, y)
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
        self.alive = True
        self.angle = angle
        self.rotated_image = pg.image.load(image)
        self.w = self.image.get_width()
        self.h = self.image.get_height()
        self.bounds = Boundaries(x=self.x,
                                 y=self.y,
                                 w=self.w,
                                 h=self.h)
        self.center = (self.x + self.w, self.y + self.h)
        self.center_x = self.x + self.w
        self.center_y = self.y + self.h
        self.last_hurt = 0
        self.screen = None
        self.left_limit = None
        self.right_limit = None
        self.top_limit = None
        self.bottom_limit = None

    def is_alive(self):
        if self.lives > 0:
            self.appear = True
            self.alive = True
            return True
        else:
            self.appear = False
            self.alive = False
            return False

    def _re_bound(self):
        self.bounds = Boundaries(x=self.x,
                                 y=self.y,
                                 w=self.w,
                                 h=self.h)

    def _move(self, x_move, y_move):
        if self.x + x_move * self.speed < self.left_limit:
            self.x = self.left_limit
        elif self.x + self.w + x_move * self.speed > self.right_limit:
            self.x = self.right_limit - self.w
        else:
            self.x += x_move * self.speed
        if self.y + y_move * self.speed < self.bottom_limit:
            self.y = self.bottom_limit
        elif self.y + self.h + y_move * self.speed > self.top_limit:
            self.y = self.top_limit - self.h
        else:
            self.y += y_move * self.speed

    def add_to_screen(self, screen):
        self.screen = screen
        self.left_limit = screen.bounds.left
        self.right_limit = screen.bounds.right
        self.top_limit = screen.bounds.top
        self.bottom_limit = screen.bounds.bottom

    def get_hurt(self, damage, recovery=3, danger=None, blowback=5):  # TODO keep player on screen
        time_since_hurt = time.perf_counter() - self.last_hurt
        if time_since_hurt > recovery:
            self.lives -= damage
            self.last_hurt = time.perf_counter()
            if self.lives > 0:
                self.alive = True
            else:
                self.alive = False
            if danger is not None:
                angle = fn.get_angle((danger.x + (danger.w / 2), danger.y + (danger.y / 2)),
                                     (self.x + (self.w / 2), self.y + (self.h / 2)), degrees=False)
                self._move(blowback * m.cos(angle), blowback * m.sin(angle))

    def is_touching(self, other):
        return fn.is_touching(self.bounds, other.bounds)


class Player(_Character):
    """
    This class defines the player of the game
    it inherits the character class
    only required input is the image to represent this player
    """
    def __init__(self,
                 image: str,
                 speed: int = 3,
                 scale: float = 1.0,
                 appear: bool = True,
                 x: float = 300.0,
                 y: float = 300.0,
                 lives: int = 3,
                 weapons: list = None,
                 angle: float = 0) -> None:
        _Character.__init__(self, x, y, lives, speed, scale, image, appear, angle)
        self.weapons = weapons
        self.fist = pg.image.load('./images/fist.png')
        self.is_player = True
        self.is_enemy = False
        self.last_punch = 0
        self.punching = False
    
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

    def update(self, screen, keys, enemies):
        for enemy in enemies:
            if self.appear:
                if self.is_touching(enemy):
                    self.get_hurt(1, recovery=1, danger=enemy, blowback=50)
        self.is_alive()
        self._get_movement(keys)
        self._re_bound()
        self._rotation_degrees()
        self.rotated_image = pg.transform.rotate(self.image, self.angle)
        offset_x, offset_y = fn.get_offset(self.image, self.rotated_image)
        screen.blit(self.rotated_image, (self.x + offset_x, self.y + offset_y))
        self.fire(screen, keys)

    def extra_life(self, life):
        self.lives += life

    def fire(self, screen, keys):
        if keys['space']:
            time_since_fire = time.perf_counter() - self.last_punch
            if self.weapons is None and (time_since_fire > 6):

                rotated_fist, pos = fn.get_orbit(self, self.fist)
                screen.blit(rotated_fist, pos)
                self.last_punch = time.perf_counter()
                self.punching = True
            elif self.weapons is None and (time_since_fire < 3):
                rotated_fist, pos = fn.get_orbit(self, self.fist)
                screen.blit(rotated_fist, pos)
                self.punching = True
            else:
                self.punching = False
        else:
            self.punching = False


class Enemy(_Character):
    def __init__(self,
                 image,
                 x=0,
                 y=0,
                 lives=1,
                 speed=2,
                 scale=1,
                 appear=True,
                 angle=0):
        _Character.__init__(self, x, y, lives, speed, scale, image, appear, angle)
        self.is_player = False
        self.is_enemy = True

    def follow(self, other):
        if other.is_player:
            if self.x + (self.w / 2) < other.x + (other.w / 2):
                self._move(1, 0)
            elif self.x + (self.w / 2) > other.x + (other.w / 2):
                self._move(-1, 0)
            if self.y + (self.h / 2) < other.y + (other.h / 2):
                self._move(0, 1)
            elif self.y + (self.h / 2) > other.y + + (other.h / 2):
                self._move(0, -1)

    # def is_hit(self, obj):
    #     if

    def update(self, screen, others): #, vector): TODO blow back from get_hurt() based on angle
        for other in others:
            # if self.is_touching(other.fist)
            if self.appear:
                self.is_alive()
        self.follow(other)
        self._re_bound()
        screen.blit(self.image, (self.x, self.y))

