from src.util.settings import *
from src.util.map import world_map
from src.util.ray_casting import mapping
from src.objects_of_game.player import Player
from src.objects_of_game.weapon import Weapon
from src.objects_of_game.interact_objects import InteractObjectsHolder
from src.renderer.drawing import Drawing
from numba import njit
import math


@njit(fastmath=True, cache=True)
def ray_casting_npc_player(npc_x, npc_y, game_map, player_position):
    ox, oy = player_position
    xm, ym = mapping(ox, oy)
    delta_x, delta_y = ox - npc_x, oy - npc_y
    cur_angle = math.atan2(delta_x, delta_y)
    cur_angle += math.pi

    sin_a = math.sin(cur_angle)
    cos_a = math.cos(cur_angle)
    sin_a = sin_a if sin_a else 0.000001
    cos_a = cos_a if cos_a else 0.000001

    # verticals
    x, dx = (xm + TILE, 1) if cos_a >= 0 else (xm, -1)
    for i in range(0, int(abs(delta_x)) // TILE):
        depth_v = (x - ox) / cos_a
        yv = oy + depth_v * sin_a
        tile_v = mapping(x + dx, yv)
        if tile_v in game_map:
            return False
        x += dx * TILE

    # horizontals
    y, dy = (ym + TILE, 1) if sin_a >= 0 else (ym, -1)
    for i in range(0, int(abs(delta_y)) // TILE):
        depth_h = (y - oy) / sin_a
        xh = ox + depth_h * cos_a
        tile_h = mapping(xh, y + dy)
        if tile_h in game_map:
            return False
        y += dy * TILE
    return True


class Interaction:
    def __init__(self, player: Player, sprites: InteractObjectsHolder, drawing: Drawing, weapon: Weapon):
        self.player = player
        self.sprites = sprites
        self.drawing = drawing
        self.weapon = weapon

    def interaction_objects(self):
        if self.player.shot and self.weapon.shot_animation_trigger:
            for obj in sorted(self.sprites.game_objects, key=lambda ob: ob.distance_to_sprite):
                if obj.is_on_fire[1]:
                    if obj.is_destroy != 'immortal' and not obj.is_destroy:
                        if ray_casting_npc_player(obj.x, obj.y, world_map, self.player.pos):
                            obj.is_destroy = True
                            obj.impassable = None
                            self.weapon.shot_animation_trigger = False
                    break

    def npc_action(self):
        for obj in self.sprites.game_objects:
            if obj.flag == 'npc' and not obj.is_destroy:
                if ray_casting_npc_player(obj.x, obj.y, world_map, self.player.pos):
                    obj.npc_action_trigger = True
                    self.npc_move(obj)
                else:
                    obj.npc_action_trigger = False

    def npc_move(self, obj):
        if obj.distance_to_sprite > TILE:
            dx = obj.x - self.player.pos[0]
            dy = obj.y - self.player.pos[1]
            obj.x = obj.x + 1 if dx < 0 else obj.x - 1
            obj.y = obj.y + 1 if dy < 0 else obj.y - 1