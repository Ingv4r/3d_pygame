import pygame as pg
from util.game_instances import GameInstanceHolder
from sprite.sprite_manager import SpriteManager
from util.settings import *
from player import Player
from renderer.drawing import Drawing
from util.ray_casting import ray_casting_walls

pg.init()
screen = pg.display.set_mode((WIDTH, HEIGHT))
pg.mouse.set_visible(False)
sc_map = pg.Surface(MINIMAP_RES)

sprite_manager = SpriteManager()
game_instance_holder = GameInstanceHolder(sprite_manager)
clock = pg.time.Clock()
player = Player(game_instance_holder)
drawing = Drawing(screen, sc_map)

while running:
    for event in pg.event.get():
        if event.type == pg.QUIT:
            exit()

    player.movement()
    screen.fill(BLACK)

    drawing.background(player.angle)
    walls = ray_casting_walls(player, drawing.textures)
    drawing.world(walls + [game_object.object_locate(player) for game_object in game_instance_holder.game_objects])
    drawing.fps(clock)
    drawing.mini_map(player)

    pg.display.flip()
    clock.tick(FPS)