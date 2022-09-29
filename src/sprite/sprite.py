import pygame
from util.position import Position
from util.settings import *

from sprite.sprite_params import SpriteParams


class Sprite:
    def __init__(self, sprite_params: SpriteParams):
        self.sprite_params = sprite_params
        self.sprite = pygame.image.load(sprite_params.path).convert_alpha()

        path = self.sprite_params.path[:-5]
        if sprite_params.has_angles:
            self.sprites = [pygame.image.load(
                f'{path}{i}.png').convert_alpha() for i in range(sprite_params.base_angles+1)]
     
        self.animation_count = 0
        self.side = 30
        self.x, self.y = 0, 0
        if sprite_params.has_angles:
            self.sprite_angles = [frozenset(range(i, i + 45))
                                  for i in range(0, 360, 45)]
            self.sprite_positions = {angle: pos for angle,
                                     pos in zip(self.sprite_angles, self.sprites)}

    