import pygame as pg
import math
from settings import *
from player import Player
from map import world_map
from drawing import Drawing

pg.init()
screen = pg.display.set_mode((WIDTH, HEIGHT))
sc_map = pg.Surface((WIDTH // MAP_SCALE, HEIGHT // MAP_SCALE))
clock = pg.time.Clock()
player = Player()
drawing = Drawing(screen, sc_map)

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

    drawing.background(player.angle)
    drawing.world(player.pos, player.angle)
    drawing.fps(clock)
    drawing.mini_map(player)



    pg.display.flip()
    clock.tick()