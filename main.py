import pygame as pg
from settings import *
from player import Player
import math

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
    screen.fill(BLACK)

    pg.draw.circle(screen, GREEN, player.pos, 8)
    pg.draw.line(
        screen, GREEN, player.pos, (player.x + WIDTH * math.cos(player.angle),
                                    player.y + WIDTH * math.sin(player.angle))
    )


    pg.display.flip()
    clock.tick(FPS)