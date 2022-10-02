import pygame
from sprite.sprite_manager import SpriteManager
from game_object import GameObject
from util.point2d import Point2d
from util.position import Position

class GameInstanceHolder():
    def __init__(self, sprite_manager: SpriteManager) -> None:
        barrel = GameObject(sprite_manager.get_sprite(SpriteManager.BARREL))
        cacodemon = GameObject(sprite_manager.get_sprite(SpriteManager.CACODEMON))
        flame = GameObject(sprite_manager.get_sprite(SpriteManager.FLAME))
        pedistal = GameObject(sprite_manager.get_sprite(SpriteManager.PEDISTAL))

        self.game_objects = [
            barrel,
            cacodemon,
            flame,
            pedistal
        ]

        barrel.update_position(Position(Point2d(4.5, 4.5)))
        cacodemon.update_position(Position(Point2d(12.5, 11.5)))
        flame.update_position(Position(Point2d(9, 13.5)))
        pedistal.update_position(Position(Point2d(8, 13.5)))

        self.collision_objects = [pygame.Rect(*[go.position.point.x, go.position.point.y], go.sprite.side, go.sprite.side) for go in
                                  self.game_objects if go.sprite.sprite_params.blocked]
