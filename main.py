import pygame as pg
import math
from settings import *
from player import Player
from map import world_map
from ray_casting import ray_casting
from drawing import Drawing

pg.init()
screen = pg.display.set_mode((WIDTH, HEIGHT))
clock = pg.time.Clock()
player = Player()
drawing = Drawing(screen)

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
    #mouse = pg.mouse.get_pos()
    screen.fill(BLACK)

    drawing.background()
    drawing.world(player.pos, player.angle)
    drawing.fps(clock)

    #pg.draw.circle(screen, GREEN, (int(player.x), int(player.y)), 8)
    #pg.draw.line(screen, GREEN, player.pos, 
    #(player.x + WIDTH * math.cos(player.angle),
    #player.y + WIDTH * math.sin(player.angle)))
#
    #for x, y in world_map:
    #    pg.draw.rect(screen, DARKGREY, (x, y, TILE, TILE), 2)


    pg.display.flip()
    clock.tick()