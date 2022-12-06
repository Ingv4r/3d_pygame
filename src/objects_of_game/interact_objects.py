import pygame
from src.objects_of_game.game_object import GameObject
from src.objects_of_game.ojects_parameters import InteractParamsHolder
from numba.core import types
from numba.typed import Dict
from numba import int32
from src.util.ray_casting import mapping


class InteractObjectsHolder:
    def __init__(self, params: InteractParamsHolder) -> None:
        barrel1 = GameObject(params.barrel, (8.5, 6.5))
        barrel2 = GameObject(params.barrel, (14.5, 6.5))
        cacodemon = GameObject(params.cacodemon, (12.5, 11.5))
        flame = GameObject(params.flame, (9, 13.5))
        pedestal = GameObject(params.pedestal, (8, 13.5))
        ghost = GameObject(params.ghost, (18, 12))
        door = GameObject(params.door, (17.5, 2.5))

        self.game_objects = [
            barrel1,
            barrel2,
            cacodemon,
            flame,
            pedestal,
            ghost,
            door
        ]

    @property
    def blocked_doors(self):
        blocked_doors = Dict.empty(key_type=types.UniTuple(int32, 2), valid_type=int32)
        for obj in self.game_objects:
            if obj.flag == 'door_v' and obj.impassable:
                i, j = mapping(obj.x, obj.y)
                blocked_doors[(i, j)] = 0
        return blocked_doors


    @property
    def collision_objects(self):
        return [pygame.Rect(*[go.x, go.y], go.side, go.side) for go in self.game_objects if go.impassable]

    @ property
    def object_hit(self):
        return min([obj.is_on_fire for obj in self.game_objects], default=(float('inf'), 0))

