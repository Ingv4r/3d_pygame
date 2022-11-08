import pygame
from sprite.sprite_params import SpriteParams
from util.settings import *


class Sprite:
    def __init__(self, sprite_params: SpriteParams):
        self.sprite_params = sprite_params
        self.sprite = pygame.image.load(sprite_params.path).convert_alpha()

        if sprite_params.has_angles:
            path = self.sprite_params.path[:-5]
            self.sprite = [pygame.image.load(
                f'{path}{i}.png').convert_alpha() for i in range(sprite_params.base_angles + 1)]
            self.sprite_angles = [frozenset(range(338, 361)) | frozenset(range(0, 23))] +\
                                 [frozenset(range(i, i + 45)) for i in range(0, 360, 45)]
            self.sprite_positions = {angle: pos for angle, pos in zip(self.sprite_angles, self.sprite)}

        self.npc_action_trigger = False
        self.dead_animation_count = 0
        self.animation_count = 0
        self.side = 30
        self.x, self.y = 0, 0
