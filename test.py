import pygame as pg
import math as m

pg.init()

FieldImg = pg.image.load("/home/pi/Desktop/room.png")
ScreenHeight = FieldImg.get_height()
ScreenWidth = FieldImg.get_width()
Screen = pg.display.set_mode((ScreenWidth, ScreenHeight))
pg.display.set_caption('Look out for those sharp guys')
PlayerImg = pg.image.load("/home/pi/Desktop/square.png")
player_pos = PlayerImg.get_rect().center
while True:
    for event in pg.event.get():
        pg.display.flip()
    Screen.fill(0)
    Screen.blit(FieldImg, (0,0))
    x1, y1 = pg.mouse.get_pos()
    x2, y2 = player_pos.center
    degrees = -m.atan2(y1-y2,x1-x2)*(360/(2*m.pi))
    rotated_img = pg.transform.rotate(PlayerImg, degrees)
    Screen.blit(pg.transform.rotate(PlayerImg, degrees), player_pos)