import pygame
from src.objects_of_game.game_object import GameObject
from src.objects_of_game.ojects_parameters import InteractParamsHolder


class InteractObjectsHolder:
    def __init__(self, params: InteractParamsHolder) -> None:
        barrel1 = GameObject(params.barrel, (8.5, 6.5))
        barrel2 = GameObject(params.barrel, (14.5, 6.5))
        cacodemon = GameObject(params.cacodemon, (12.5, 11.5))
        flame = GameObject(params.flame, (9, 13.5))
        pedestal = GameObject(params.pedestal, (8, 13.5))
        ghost = GameObject(params.ghost, (18, 12))

        self.game_objects = [
            barrel1,
            barrel2,
            cacodemon,
            flame,
            pedestal,
            ghost
        ]

    @property
    def collision_objects(self):
        return [pygame.Rect(*[go.x, go.y], go.side, go.side) for go in self.game_objects if go.impassable]

    @ property
    def object_hit(self):
        return min([obj.is_on_fire for obj in self.game_objects], default=(float('inf'), 0))

