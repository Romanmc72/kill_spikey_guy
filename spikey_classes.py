import pygame as pg
import functions as fn
import sys
import time
import math as m
import numpy.random as r
import re
import os
# from pg.locals import *
# TODO generate enemies after they die
# TODO set varying levels of comebacks after score is calculated
# TODO create weapons
# TODO create projectiles
# TODO create heat-seeking projectiles
# TODO create animations with walking and fighting
# TODO include audio sound-fx & songs based on package
# TODO Explore a /giphy API to see if insults can be paired with `.gifs`
# TODO enable cheat codes to make the explicit and mean options auto-magic
# TODO make a `meatspin` cheat if possible
# TODO allow reflexive resizing of images to ensure all games function the same


def get_package_option(spacing=10) -> list:
    cheats = []
    options = os.listdir('./images')
    num_options = len(options)
    font = pg.font.SysFont('Times New Roman', 25)
    rendered_options = [font.render(f'[{option_number}] : {option}', False, (255, 255, 0))
                        for option_number, option in
                        enumerate(options)]
    rendered_option_height = rendered_options[0].get_height()
    longest_option = max([option.get_width() for option in rendered_options])
    w = longest_option + 2 * spacing
    h = (rendered_option_height * num_options) + (spacing * (num_options + 1))
    # screen = pg.display.set_mode((w, h))
    screen = pg.display.set_mode((0, 0))
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
                    cheats = cheat_menu()
    return [options[option_number]] + cheats


def cheat_menu() -> list:
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


class Package:
    """
    which set of images will be imported for this game?
    set the name as the name of the package you wish to import.
    Packages are listed in the './images/ folder.
    """
    def __init__(self):
        pack = get_package_option()
        self.name = pack[0]
        self.enemy = f'./images/{self.name}/enemy.png'
        self.player = f'./images/{self.name}/player.png'
        self.background = f'./images/{self.name}/background.png'
        self.fist = f'./images/{self.name}/fist.png'
        self.cheats = pack[1:]


class Game:
    def __init__(self,
                 done: bool = False,
                 characters: list = []) -> None:
        pg.init()
        self.package = Package()
        self.background = pg.transform.scale(pg.image.load(self.package.background), (800, 800))
        self.done = done
        self.characters = characters
        self.mean = (True if ':(' in self.package.cheats else False)
        self.explicit = (True if '>:(' in self.package.cheats else False)
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
        # enemies = [character for character in self.characters if character.is_enemy and character.alive]
        enemies = []
        for index, character in enumerate(self.characters):
            if character.is_enemy and character.alive:
                enemies.append(character)
            elif character.is_enemy and not character.alive:
                self.characters.pop(index)
        players = [character for character in self.characters if character.is_player and character.alive]
        for player in players:
            player.update(self.screen, self.key_state, enemies)
            for life in range(player.lives):
                self.screen.blit(pg.transform.scale(player.image, (20, 20)), (25 + 20 * life, 25))
        for enemy in enemies:
            self.score += enemy.update(self.screen, players)
            for life in range(enemy.lives):
                self.screen.blit(pg.transform.scale(enemy.image, (20, 20)), (self.w - 25 - 20 * life, 25))
        if not players:
            self.done = True
        for player in players:
            if not player.alive:
                self.done = True
        if not enemies:
            for additional in range(self.enemies):
                enemy = Enemy(self.package.enemy, speed=r.choice(5))
                self.add_character(enemy)
            self.enemies += 1

    def show_score(self):
        font = pg.font.SysFont('Arial', 30)
        text = font.render(f"Score: {self.score}", False, (255, 0, 0))
        self.screen.blit(text, (self.center_x, 25))

    def play(self):
        player = Player(self.package.player, self.package.fist)
        enemy = Enemy(self.package.enemy)
        self.add_character(player)
        self.add_character(enemy)
        self.enemies += 1
        while not self.done:
            for event in pg.event.get():
                self.get_keys(event=event)
                if event.type == pg.QUIT:
                    self.done = True
                elif event.type == pg.KEYDOWN:
                    if event.key == pg.K_ESCAPE:
                        self.done = True
            self.screen.fill(0)
            self.screen.blit(self.background, (0, 0))
            self.screen.blit(self.background, (0, 0))
            self.update_characters()
            self.show_score()
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

    def hurl_insults(self):
        insults = ['Maybe next time']
        if self.mean:
            insults += ['You really suck at this',
                        'The worst performance in the history of performances. Ever.',
                        'Awful',
                        'Disgraceful!',
                        'You call that trying?',
                        'BOOOOO YOU STINK!!!',
                        'I\'ve never seen worse',
                        'Nice try. NOT!',
                        'ha ha',
                        'Loser',
                        'You gonna cry? :(',
                        'It\'s like you don\'t even care...']
        if self.explicit:
            insults += ['Eat it bitch',
                        'Fuck outta here if you gonna sucka dick',
                        'Choked a big one',
                        'u suck ass',
                        'shitty performance',
                        'Bitch',
                        'fuck you motherfucker',
                        'u piece of shit']
        font = pg.font.SysFont('Times New Roman', 25)
        game_over = font.render(f'GAME OVER, score:{self.score}', False, (255, 255, 0))
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

    def hurl_meh(self):
        insults = ['I guess that was okay']
        if self.mean:
            insults += ['at least you tried this time',
                        'I have see worse.',
                        'Not totally disappointing',
                        'I still think you could do better']
        if self.explicit:
            insults += ['Big fuckin woop',
                        'Yeah you got a few points. You still a Bitch tho',
                        'Not a total fucking failure',
                        'almost a decent score, asshole.',
                        'Choked a smaller dick this time']
        font = pg.font.SysFont('Times New Roman', 25)
        game_over = font.render(f'GAME OVER, score:{self.score}', False, (255, 255, 0))
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

    def hurl_impressed(self):
        insults = ['Nicely done']
        if self.mean:
            insults += ['I have nothing negative to say']
        if self.explicit:
            insults += ['Nice job. Bitch']
        font = pg.font.SysFont('Times New Roman', 25)
        game_over = font.render(f'GAME OVER, score:{self.score}', False, (255, 255, 0))
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

    def hurl_damn_son(self):
        insults = ['Speechless',
                   '*standing-ovation*']
        if self.mean:
            insults += ['bet you feel proud of yourself',
                        'Congrats on your huge waste of time',
                        'Don\'t you have better things to do?']
        if self.explicit:
            insults += ['Damn son, you cheatin?',
                        'You probably cheated, Bitch']
        font = pg.font.SysFont('Times New Roman', 25)
        game_over = font.render(f'GAME OVER, score:{self.score}', False, (255, 255, 0))
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
        if self.score < 100:
            self.hurl_insults()
        elif 100 <= self.score < 200:
            self.hurl_meh()
        elif 200 <= self.score < 500:
            self.hurl_impressed()
        else:
            self.hurl_damn_son()

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
                 image: str,
                 fist: str,
                 speed: int = 5,
                 scale: float = 1.0,
                 appear: bool = True,
                 x: float = 300.0,
                 y: float = 300.0,
                 lives: int = 3,
                 weapons: list = None,
                 angle: float = 0) -> None:
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
            if self.appear:
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

    def add_to_screen(self, screen, x=None, y=None):
        self.screen = screen
        self.left_limit = screen.bounds.left
        self.right_limit = screen.bounds.right
        self.top_limit = screen.bounds.top
        self.bottom_limit = screen.bounds.bottom
        self.x = (r.choice(self.right_limit - self.w) if x is None else x)
        self.y = (r.choice(self.top_limit - self.h) if y is None else y)

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
