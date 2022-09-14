import pygame as pg
from settings import *
from player import Player
from drawing import Drawing
from sprite_objects import *
from ray_casting import ray_casting

pg.init()
screen = pg.display.set_mode((WIDTH, HEIGHT))
pygame.mouse.set_visible(False)
sc_map = pg.Surface(MINIMAP_RES)

sprites = Sprites()
clock = pg.time.Clock()
player = Player()
drawing = Drawing(screen, sc_map)

while running:
    for event in pg.event.get():
        if event.type == pg.QUIT:
            running = False
            exit()

    player.movement()
    #mouse = pg.mouse.get_pos()
    screen.fill(BLACK)

    drawing.background(player.angle)
    walls = ray_casting(player, drawing.textures)
    drawing.world(walls + [obj.object_locate(player) for obj in sprites.list_of_objects])
    drawing.fps(clock)
    drawing.mini_map(player)



    pg.display.flip()
    clock.tick()