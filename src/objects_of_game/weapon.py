import pygame
from collections import deque
from src.util.settings import *


class Weapon:
    def __init__(self):
        # weapon parameters
        directory = 'res/sprites/weapons/'
        self.weapon_base_sprite = pygame.image.load(
            f'{directory}shotgun/base/0.png').convert_alpha()
        num_of_png = 20
        self.weapon_shot_animation = deque(
            [pygame.image.load(f'{directory}shotgun/shot/{i}.png').convert_alpha()
             for i in range(num_of_png)])
        self.weapon_rect = self.weapon_base_sprite.get_rect()
        self.weapon_pos = (HALF_WIDTH - self.weapon_rect.width // 2,
                           HEIGHT - self.weapon_rect.height)
        self.shot_length = len(self.weapon_shot_animation)
        self.shot_length_count = 0
        self.shot_animation_speed = 3
        self.shot_animation_count = 0
        self.shot_animation_trigger = True
        # sfx parameters
        self.sfx = deque(
            [pygame.image.load(f'{directory}sfx/{i}.png').convert_alpha()
             for i in range(9)])
        self.sfx_length_count = 0
        self.sfx_length = len(self.sfx)
