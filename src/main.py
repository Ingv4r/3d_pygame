import pygame as pg
from util.settings import *
from util.game_instances import GameInstanceHolder
from sprite.sprite_manager import SpriteManager
from player import Player
from weapon import Weapon
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
weapon = Weapon()
drawing = Drawing(screen, sc_map, player, weapon)

while running:
    player.movement()

    drawing.background(player.angle)
    walls, wall_shot = ray_casting_walls(player, drawing.textures)
    drawing.world(walls + [game_object.object_locate(player) for game_object in game_instance_holder.game_objects])
    drawing.fps(clock)
    drawing.mini_map(player)
    drawing.player_weapon([wall_shot, game_instance_holder.object_hit])

    pg.display.flip()
    clock.tick(FPS)
