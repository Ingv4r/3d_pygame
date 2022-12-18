import pygame as pg
from src.util.settings import *
from src.objects_of_game.interact_objects import InteractObjectsHolder
from src.objects_of_game.ojects_parameters import InteractParamsHolder
from src.objects_of_game.player import Player
from src.objects_of_game.weapon import Weapon
from src.renderer.drawing import Drawing, DrawingMenu
from src.util.ray_casting import ray_casting_walls
from src.util.interaction import Interaction

pg.init()
screen = pg.display.set_mode((WIDTH, HEIGHT))
sc_map = pg.Surface(MINIMAP_RES)

params = InteractParamsHolder()
int_obj_holder = InteractObjectsHolder(params)
clock = pg.time.Clock()
player = Player(int_obj_holder)
weapon = Weapon()
drawing = Drawing(screen, sc_map, player, weapon, clock)
drawing_menu = DrawingMenu(screen, clock)
interaction = Interaction(player, int_obj_holder, drawing, weapon)

drawing_menu.menu_loop()
pg.mouse.set_visible(False)
interaction.play_sound()


def game_loop():
    while running:
        player.movement()

        drawing.background(player.angle)
        walls, wall_shot = ray_casting_walls(player, drawing.textures)
        drawing.world(walls + [game_object.object_locate(player) for game_object in int_obj_holder.game_objects])
        drawing.fps(clock)
        drawing.mini_map(player)
        drawing.player_weapon([wall_shot, int_obj_holder.object_hit])

        interaction.interaction_objects()
        interaction.npc_action()
        interaction.clear_world()
        interaction.check_win()

        pg.display.flip()
        clock.tick(FPS)


if __name__ == '__main__':
    game_loop()
