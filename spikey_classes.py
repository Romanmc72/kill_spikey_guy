#!/usr/bin/env python3
"""
This is a hodgepodge of classes and objects necessary for the game.
There is much to add and much refactoring to do, but it works so that is happy.
"""
import sys
import time
import math as m
import random as r
import re
import os

import pygame as pg

import spikey_messages
import spikey_functions as fn
# TODO create weapons
# TODO create projectiles
# TODO create heat-seeking projectiles
# TODO create animations with walking and fighting
# TODO include audio sound-fx & songs based on package
# TODO Include a `.gif` into the game somewhere
# TODO break down a `.gif` into frames and animate it into reality
# TODO allow reflexive resizing of images to ensure all games function the same despite what gets imported
# TODO make a `meatspin` cheat if possible
# TODO make safe zone in the middle of the screen so you don't get spawned on
# TODO recovery health bar

DEFAULT_WIDTH = 1300
DEFAULT_HEIGHT = 650


class Package:
    """
    which set of images will be imported for this game?
    set the name as the name of the package you wish to import.
    Packages are listed in the './images/ folder.
    """
    def __init__(self):
        pack = self.get_package_option()
        self.name = pack[0]
        self.enemy = './images/{}/enemy.png'.format(self.name)
        self.player = './images/{}/player.png'.format(self.name)
        self.background = './images/{}/background.png'.format(self.name)
        self.fist = './images/{}/fist.png'.format(self.name)
        self.cheats = pack[1:]

    def get_package_option(self, spacing=10):
        cheats = []
        options = os.listdir('./images')
        num_options = len(options)
        font = pg.font.SysFont('Times New Roman', 25)
        rendered_options = [font.render('[{option_number}] : {option}'.format(option_number=option_number, option=option), False, (255, 255, 0))
                            for option_number, option in
                            enumerate(options)]
        rendered_option_height = rendered_options[0].get_height()
        longest_option = max([option.get_width() for option in rendered_options])
        w = DEFAULT_WIDTH
        h = DEFAULT_HEIGHT
        screen = pg.display.set_mode((w, h))
        screen.fill(0)
        [screen.blit(option, (spacing, spacing + (option_number * rendered_option_height)))
        for option_number, option in
        enumerate(rendered_options)]
        pg.display.flip()
        nothing_pressed = True
        while nothing_pressed:
            for event in pg.event.get():
                if event.type == pg.KEYDOWN:
                    if event.key == pg.K_ESCAPE:
                        pg.quit()
                        sys.exit()
                    elif event.key == pg.K_0 and num_options > 0:
                        option_number = 0
                        nothing_pressed = False
                    elif event.key == pg.K_1 and num_options > 1:
                        option_number = 1
                        nothing_pressed = False
                    elif event.key == pg.K_2 and num_options > 2:
                        option_number = 2
                        nothing_pressed = False
                    elif event.key == pg.K_3 and num_options > 3:
                        option_number = 3
                        nothing_pressed = False
                    elif event.key == pg.K_4 and num_options > 4:
                        option_number = 4
                        nothing_pressed = False
                    elif event.key == pg.K_5 and num_options > 5:
                        option_number = 5
                        nothing_pressed = False
                    elif event.key == pg.K_6 and num_options > 6:
                        option_number = 6
                        nothing_pressed = False
                    elif event.key == pg.K_7 and num_options > 7:
                        option_number = 7
                        nothing_pressed = False
                    elif event.key == pg.K_8 and num_options > 8:
                        option_number = 8
                        nothing_pressed = False
                    elif event.key == pg.K_9 and num_options == 10:
                        option_number = 9
                        nothing_pressed = False
                    elif event.key == pg.K_c:
                        cheats = self.cheat_menu()
        return [options[option_number]] + cheats

    def cheat_menu(self):
        cheating = True
        cheats = []
        while cheating:
            code = [input("ENTER CHEAT CODE\n(enter 'q' to exit)\n: ")]
            # if code == 'q':
            if 'q' in code:
                cheating = False
            else:
                cheats += code
        return cheats

class Game:
    def __init__(self,
                 done = False,
                 characters = []):
        pg.init()
        self.x = 0
        self.y = 0
        self.w = DEFAULT_WIDTH
        self.h = DEFAULT_HEIGHT
        self.package = Package()
        self.background = pg.transform.scale(pg.image.load(self.package.background), (self.w, self.h))

        self.done = done
        self.characters = characters
        self.mean = (True if ':(' in self.package.cheats else False)
        self.explicit = (True if '>:(' in self.package.cheats else False)
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
        self.center = (self.x + (self.w / 2), self.y + (self.h / 2))
        self.center_x = self.center[0]
        self.center_y = self.center[1]
        self.score = 0
        self.enemies = 1
        print('mean') if self.mean else None
        print('explicit') if self.explicit else None

    def add_character(self, character):
        self.characters.append(character)
        character.add_to_screen(self)

    def remove_character(self, character):
        self.characters.pop(self.characters.index(character))

    def update_characters(self):
        enemies = [character for character in self.characters if character.is_enemy and character.alive]
        dead = [character for character in self.characters if character.is_enemy and not character.alive]
        [self.remove_character(character) for character in dead[::-1]]
        players = [character for character in self.characters if character.is_player and character.alive]
        for player in players:
            player.update(self.screen, self.key_state, enemies)
            for life in range(player.lives):
                self.screen.blit(pg.transform.scale(player.image, (20, 20)), (25 + 20 * life, 25))
        for enemy in enemies:
            self.score += enemy.update(self.screen, players)
        if not players:
            self.done = True
        for player in players:
            if not player.alive:
                self.done = True
        if not enemies:
            for additional in range(self.enemies):
                enemy = Enemy(self.package.enemy, speed=r.choice(range(1, 5)))
                self.add_character(enemy)
            self.enemies += 1

    def show_score(self):
        font = pg.font.SysFont('Arial', 30)
        text = font.render("Score: {}".format(self.score), False, (255, 0, 0))
        self.screen.blit(text, (self.center_x, 25))

    def play(self):
        player = Player(self.package.player, self.package.fist)
        enemy = Enemy(self.package.enemy)
        self.add_character(player)
        self.add_character(enemy)
        self.enemies += 1
        pg.display.set_mode((self.w, self.h))
        while not self.done:
            for event in pg.event.get():
                self.get_keys(event=event)
                if event.type == pg.QUIT:
                    self.done = True
                elif event.type == pg.KEYDOWN:
                    if event.key == pg.K_ESCAPE:
                        self.done = True
            self.screen.fill([0, 0, 0])
            self.screen.blit(self.background, (0, 0))
            # self.screen.blit(self.background, self.background_rect)
            self.update_characters()
            self.show_score()
            pg.display.flip()
            pg.display.update()

        self.__end__()

    def get_keys(self, event):
        if event.type == pg.KEYDOWN:
            if event.key in [pg.K_d, pg.K_RIGHT]:
                self.key_state['right'] = True
            elif event.key in [pg.K_a, pg.K_LEFT]:
                self.key_state['left'] = True
            elif event.key in [pg.K_w, pg.K_UP]:
                self.key_state['up'] = True
            elif event.key in [pg.K_s, pg.K_DOWN]:
                self.key_state['down'] = True
            elif event.key == pg.K_SPACE:
                self.key_state['space'] = True
        elif event.type == pg.KEYUP:
            if event.key in [pg.K_d, pg.K_RIGHT]:
                self.key_state['right'] = False
            elif event.key in [pg.K_a, pg.K_LEFT]:
                self.key_state['left'] = False
            elif event.key in [pg.K_w, pg.K_UP]:
                self.key_state['up'] = False
            elif event.key in [pg.K_s, pg.K_DOWN]:
                self.key_state['down'] = False
            elif event.key == pg.K_SPACE:
                self.key_state['space'] = False

    def _display_end_game_message(self):
        if self.explicit:
            insults = spikey_messages.explicit_message
        elif self.mean:
            insults = spikey_messages.mean_message
        else:
            insults = spikey_messages.normal_message
        
        if self.score < 100:
            insults = insults.insult
        elif 100 <= self.score < 200:
            insults = insults.meh
        elif 200 <= self.score < 500:
            insults = insults.impressed
        else:
            insults.damn_son

        font = pg.font.SysFont('Times New Roman', 25)
        game_over = font.render('GAME OVER, score:{}'.format(self.score), False, (255, 255, 0))
        esc = font.render('Press \'esc\' to exit.', False, (255, 255, 0))
        drop = game_over.get_height() + 10
        words = [font.render(insult, False, (255, 255, 0)) for insult in
                 [word for word in re.split(r'\s', (r.choice(insults)))]]
        words.append(esc)
        self.done = False
        while not self.done:
            for event in pg.event.get():
                self.get_keys(event=event)
                if event.type == pg.QUIT:
                    self.done = True
                elif event.type == pg.KEYDOWN:
                    if event.key == pg.K_ESCAPE:
                        self.done = True
            self.screen.fill(0)
            self.screen.blit(game_over, (5, 5))
            [self.screen.blit(words[word], (5, words[word].get_height() * word + drop)) for word in range(len(words))]
            pg.display.flip()

    def __end__(self):
        self._display_end_game_message()
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
                 x,
                 y,
                 lives,
                 speed,
                 scale,
                 image,
                 appear,
                 angle):
        self.x = x
        self.y = y
        self.lives = lives
        self.speed = speed
        self.scale = scale
        self.image = pg.transform.scale(pg.image.load(image), (100, 100))
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
        self.dangerous = False
        self.alive_since = time.perf_counter()

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
        # Keep player on screen on x-axis
        if self.x + x_move * self.speed < self.left_limit:
            self.x = self.left_limit
        elif self.x + self.w + x_move * self.speed > self.right_limit:
            self.x = self.right_limit - self.w
        else:
            self.x += x_move * self.speed
        # Keep player on screen on y-axis
        if self.y + y_move * self.speed < self.bottom_limit:
            self.y = self.bottom_limit
        elif self.y + self.h + y_move * self.speed > self.top_limit:
            self.y = self.top_limit - self.h
        else:
            self.y += y_move * self.speed
        self.center = (self.x + (self.w / 2), self.y + (self.h / 2))
        self.center_x = self.x + (self.w / 2)
        self.center_y = self.y + (self.h / 2)

    def add_to_screen(self, screen):
        self.screen = screen
        self.left_limit = screen.bounds.left
        self.right_limit = screen.bounds.right
        self.top_limit = screen.bounds.top
        self.bottom_limit = screen.bounds.bottom

    def get_hurt(self, damage, recovery=3, danger=None, blowback=5):
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
            return True
        else:
            return False

    def is_touching(self, other):
        return fn.is_touching(self.bounds, other.bounds)


class Player(_Character):
    """
    This class defines the player of the game
    it inherits the character class
    only required input is the image to represent this player
    """
    def __init__(self,
                 image,
                 fist,
                 speed = 5,
                 scale = 1.0,
                 appear = True,
                 x = 300.0,
                 y = 300.0,
                 lives = 3,
                 weapons = None,
                 angle = 0):
        _Character.__init__(self, x, y, lives, speed, scale, image, appear, angle)
        self.fist = pg.transform.scale(pg.image.load(fist), (50, 100))
        self.weapons = weapons
        self.fist_length = self.fist.get_width()
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
            if self.appear and enemy.dangerous:
                if self.is_touching(enemy):
                    self.get_hurt(1, recovery=3, danger=enemy, blowback=20)
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

    def fire(self, screen, keys, duration=0.5, recovery=0):
        if keys['space']:
            time_since_fire = time.perf_counter() - self.last_punch
            if self.weapons is None and (time_since_fire > recovery):

                rotated_fist, pos = fn.get_orbit(self, self.fist)
                screen.blit(rotated_fist, pos)
                self.last_punch = time.perf_counter()
                self.punching = True
            elif self.weapons is None and (time_since_fire < duration):
                rotated_fist, pos = fn.get_orbit(self, self.fist)
                screen.blit(rotated_fist, pos)
                self.punching = True
            else:
                self.punching = False
        else:
            self.punching = False


class Enemy(_Character):
    """
    an extension of the _Character class
    whose movement follows the Player object
    within the Game object and whose
    get_hurt() method is called based on intersection
    with certain player attributes and methods.

    Enemy will spawn randomly within the screen
    unless otherwise specified when using the
    add_to_screen() method
    """
    def __init__(self,
                 image,
                 x=0,
                 y=0,
                 lives=3,
                 speed=2,
                 scale=1,
                 appear=True,
                 angle=0):
        _Character.__init__(self, x, y, lives, speed, scale, image, appear, angle)
        self.is_player = False
        self.is_enemy = True
        self.point = False
        self.harmless_for = 1

    def add_to_screen(self, screen, x=None, y=None):
        self.screen = screen
        self.left_limit = screen.bounds.left
        self.right_limit = screen.bounds.right
        self.top_limit = screen.bounds.top
        self.bottom_limit = screen.bounds.bottom
        self.x = (r.randint(0, self.right_limit - self.w) if x is None else x)
        self.y = (r.randint(0, self.top_limit - self.h) if y is None else y)

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

    def update(self, screen, others):
        if time.perf_counter() - self.alive_since > self.harmless_for:
            self.dangerous = True
        for other in others:
            if other.punching and \
                    fn.is_facing(other, self, 45) and \
                    fn.get_distance(self.center, other.center) <= other.fist_length + ((other.w + self.w) / 2):
                    self.point = self.get_hurt(damage=1, recovery=0, danger=other, blowback=50)
            if self.appear:
                self.is_alive()
        self.follow(other)
        self._re_bound()
        screen.blit(self.image, (self.x, self.y))
        if self.point:
            self.point = False
            return 1
        else:
            return 0


class Projectile:
    """
    These are intended to be launched from
    some fixed point to another point
    that is either fixed or moving
    """
    def __init__(self, image, start, end, tracking=False, speed=1):
        self.image = pg.image.load(image)
        self.start = start
        self.end = end
        self.tracking = tracking
        self.speed = speed
        self.x = start[0]
        self.y = start[1]
        self.w = self.image.get_width()
        self.h = self.image.get_height()
        self.bounds = Boundaries(x=self.x,
                                 y=self.y,
                                 w=self.w,
                                 h=self.h)


class PowerUp:
    def __init__(self, power):
        self.power = power


class HUDBar:
    def __init__(self, start, maximum = 100, minimum = 0, percent = True):
        self.start = start
        self.maximum = maximum
        self.minimum = minimum
        self.percent = percent
        self.empty_color = (255, 0, 0)
        self.full_color = (0, 255, 0)
        self.over_charge_color = (0, 255, 255)

