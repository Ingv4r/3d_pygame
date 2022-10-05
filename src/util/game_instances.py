import pygame
from sprite.sprite_manager import SpriteManager
from util.point2d import Point2d
from util.position import Position
from game_object import GameObject


class GameInstanceHolder:
    def __init__(self, sprite_manager: SpriteManager) -> None:
        barrel1 = (GameObject(sprite_manager.get_sprite(SpriteManager.BARREL)), 7.5, 6.5)
        barrel2 = (GameObject(sprite_manager.get_sprite(SpriteManager.BARREL)), 16.5, 6.5)
        cacodemon = (GameObject(sprite_manager.get_sprite(SpriteManager.CACODEMON)), 12.5, 11.5)
        flame = (GameObject(sprite_manager.get_sprite(SpriteManager.FLAME)), 9, 13.5)
        pedistal = (GameObject(sprite_manager.get_sprite(SpriteManager.PEDISTAL)), 8, 13.5)

        self.game_objects = []
        self.add_objects_and_positions(barrel1, barrel2, cacodemon, flame, pedistal)

        self.collision_objects = [
            pygame.Rect(*[go.position.point.x, go.position.point.y], go.sprite.side, go.sprite.side) for go in
            self.game_objects if go.sprite.sprite_params.blocked
        ]

    @property
    def sprite_shot(self):
        return min([obj.is_on_fire for obj in self.game_objects], default=(float('inf'), 0))

    def add_objects_and_positions(self, *objects: tuple) -> None:
        for obj in objects:
            self.game_objects.append(obj[0])
            obj[0].update_position(Position(Point2d(obj[1], obj[2])))
