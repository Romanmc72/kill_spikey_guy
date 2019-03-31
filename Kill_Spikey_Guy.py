import pygame, sys
from pygame.locals import *
import math
import time as tm

###Start Game####################
pygame.init()   #################
#################################
###Images Representing Objects###
PlayerImg = pygame.image.load("/home/pi/Desktop/circle.png")
FieldImg = pygame.image.load("/home/pi/Desktop/room.png")
SpikeyGuyImg = pygame.image.load("/home/pi/Desktop/sharp.png")
FistImg =  pygame.image.load("/home/pi/Desktop/fist.png")

ScreenHeight = FieldImg.get_height()
ScreenWidth = FieldImg.get_width()
Screen = pygame.display.set_mode((ScreenWidth, ScreenHeight))
pygame.display.set_caption('Look out for those sharp guys')
#################################
#################################
###Game Functions################
def FIRE(Wpn):
    if Wpn == 0:
        Punch()
    else:
        Shoot()

def Punch():
    return 0

def Shoot():
    return 0

###Player, Weapon, Enemy Attributes##############
Play = True
RangeMult = 1

class Player(pygame.sprite.Sprite):
    def __init__(self):
         self.x = 300
         self.y = 300
         self.lives = 3
         self.weapon = 0
         self.speed = 1
         self.angle = 1
         self.size = 1
         self.image = PlayerImg
    def __str__(self):
        return "[x="+self.x+";"+"y="+self.y+";"+"lives="+self.lives+";"+"weapon="+self.weapon+";"+"speed="+self.speed+";"+"angle="+self.angle+";"+"size="+self.size+"]"
    def Rotate(self):
        x1 = pygame.mouse.get_pos()[0]
        x2 = self.x
        y1 = pygame.mouse.get_pos()[1]
        y2 = self.y
        return math.atan2(y1-y2,x1-x2)
    def Move(self):
        if pygame.key.get_pressed()[K_LEFT] == True or pygame.key.get_pressed() == [K_a]:
            self.x -= 5
        if pygame.key.get_pressed()[K_RIGHT] == True or pygame.key.get_pressed() == [K_d]:
            self.x += 5
        if pygame.key.get_pressed()[K_UP] == True  or pygame.key.get_pressed() == [K_w]:
            self.y -= 5
        if pygame.key.get_pressed()[K_DOWN] == True or pygame.key.get_pressed() == [K_s]:
            self.y += 5
    def Draw(self):
        Screen.blit(self.image,(self.x,self.y))

PlayerOne = Player()

Play = True

while Play:
    for event in pygame.event.get():
        pygame.display.flip()
    Screen.fill(0)
    Screen.blit(FieldImg, (0,0))
    PlayerOne.Move()
    PlayerOne.Draw()
    
    if PlayerOne.lives <= 0:
        Play = False
        
    
    
    
    
    
    