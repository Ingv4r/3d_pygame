import pygame as pg
from settings import *
from player import Player
import math
from map import world_map

pg.init()
screen = pg.display.set_mode((WIDTH, HEIGHT))
clock = pg.time.Clock()
player = Player()

while running:
    for event in pg.event.get():
        if event.type == pg.QUIT:
            running = False
            exit()
        elif event.type == pg.KEYDOWN:
            if event.key == pg.K_ESCAPE:
                running = False
                exit()
    player.movement()
    mouse = pg.mouse.get_pos()
    screen.fill(BLACK)

    pg.draw.circle(screen, GREEN, player.pos, 8)
    pg.draw.line(screen, GREEN, player.pos, mouse)
    for x, y in world_map:
        pg.draw.rect(screen, DARKGREY, (x, y, TITLE, TITLE), 2)


    pg.display.flip()
    clock.tick(FPS)