import pygame as pg
import math as m

pg.init()

FieldImg = pg.image.load("./images/room.png")
ScreenHeight = FieldImg.get_height()
ScreenWidth = FieldImg.get_width()
Screen = pg.display.set_mode((ScreenWidth, ScreenHeight))
pg.display.set_caption('Look out for those sharp guys')
PlayerImg = pg.image.load("./images/fist.png")


# Player_h = PlayerImg.get_height()
# Player_w = PlayerImg.get_width()
# max_offset_h = (Player_h*(2**.5)-Player_h)/2
# max_offset_w = (Player_w*(2**.5)-Player_w)/2


player_pos = PlayerImg.get_rect()

done = False
while not done:
    for event in pg.event.get():
        if event.type == pg.QUIT:
            done = True
        elif event.type == pg.KEYDOWN:
            if event.key == pg.K_ESCAPE:
                done = True

    Screen.fill(0)
    Screen.blit(FieldImg, (0, 0))
    x1, y1 = pg.mouse.get_pos()
    x2, y2 = player_pos.center
    degrees = -m.atan2(y1-y2,x1-x2)*(360/(2*m.pi))
    rotated_img = pg.transform.rotate(PlayerImg, degrees)
    rotated_rect = rotated_img.get_rect()

    original_center = player_pos.center
    rotated_center = rotated_rect.center

    offset_x = original_center[0] - rotated_center[0]
    offset_y = original_center[1] - rotated_center[1]

    rotated_pos = (
        player_pos[0] + offset_x,
        player_pos[1] + offset_y)
    Screen.blit(rotated_img, rotated_pos)
    pg.display.flip()

pg.quit()
