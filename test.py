import pygame as pg
import math as m

pg.init()

FieldImg = pg.image.load("room.png")
ScreenHeight = FieldImg.get_height()
ScreenWidth = FieldImg.get_width()
Screen = pg.display.set_mode((ScreenWidth, ScreenHeight))
pg.display.set_caption('Look out for those sharp guys')
PlayerImg = pg.image.load("circle.png")
Player_h = PlayerImg.get_height()
Player_w = PlayerImg.get_width()
max_offset_h = (Player_h*(2**.5)-Player_h)/2
max_offset_w = (Player_w*(2**.5)-Player_w)/2
player_pos = PlayerImg.get_rect()
while True:
    for event in pg.event.get():
        pg.display.flip()
    Screen.fill(0)
    Screen.blit(FieldImg, (0,0))
    x1, y1 = pg.mouse.get_pos()
    x2, y2 = player_pos.center
    degrees = -m.atan2(y1-y2,x1-x2)*(360/(2*m.pi))
    rotated_img = pg.transform.rotate(PlayerImg, degrees)
    conversion = abs(m.sin(degrees*(m.pi/180)*2))
    offset_h = conversion * max_offset_h
    offset_w = conversion * max_offset_w
    rotated_pos = (
        player_pos[0] - offset_h,
        player_pos[1] - offset_w)
    Screen.blit(rotated_img, rotated_pos)

