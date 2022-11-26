from collections import deque
import pygame


class InteractParamsHolder:
    def __init__(self):
        self.barrel = BarrelParams()
        self.flame = FlameParams()
        self.ghost = GhostParams()
        self.cacodemon = CacodemonParams()
        self.pedestal = PedestalParams()


class BarrelParams:
    def __init__(self) -> None:
        self.sprite = pygame.image.load('res/sprites/barrel/base/0.png').convert_alpha()
        self.shift = 1.8
        self.scale = (0.4, 0.4)
        self.side = 30
        self.animation = deque(
            [pygame.image.load(f'res/sprites/barrel/anim/{i}.png').convert_alpha() for i in range(12)]
        )
        self.destroy_animation = deque(
            [pygame.image.load(f'res/sprites/barrel/death/{i}.png').convert_alpha() for i in range(4)]
        )
        self.destroy_shift = 10.0
        self.animation_dist = 800
        self.animation_speed = 10
        self.impassable = True
        self.flag = 'decor'
        check_params(self)


class CacodemonParams:
    def __init__(self) -> None:
        self.sprite = [pygame.image.load(f'res/sprites/npc/cacodemon/base/{i}.png').convert_alpha() for i in range(8)]
        self.viewing_angles = True
        self.shift = 0.0
        self.scale = (1.1, 1.1)
        self.side = 50
        self.destroy_animation = deque(
            [pygame.image.load(f'res/sprites/npc/cacodemon/death/{i}.png').convert_alpha() for i in range(6)])
        self.destroy_shift = 0.6
        self.animation_dist = None
        self.animation_speed = 10
        self.impassable = True
        self.flag = 'npc'
        self.obj_attack = deque(
            [pygame.image.load(f'res/sprites/npc/cacodemon/anim/{i}.png').convert_alpha() for i in range(9)])
        check_params(self)


class FlameParams:
    def __init__(self) -> None:
        self.sprite = pygame.image.load('res/sprites/flame/base/0.png').convert_alpha()
        self.shift = 0.7
        self.scale = (0.6, 0.6)
        self.side = 30
        self.animation = deque(
            [pygame.image.load(f'res/sprites/flame/anim/{i}.png').convert_alpha() for i in range(16)])
        self.is_destroy = 'immortal'
        self.animation_dist = 1800
        self.animation_speed = 5
        self.flag = 'decor'
        check_params(self)


class PedestalParams:
    def __init__(self) -> None:
        self.sprite = pygame.image.load('res/sprites/pedestal/base/0.png').convert_alpha()
        self.shift = 1.8
        self.scale = (0.4, 0.4)
        self.side = 30
        self.animation_dist = 800
        self.animation_speed = 10
        self.is_destroy = 'immortal'
        self.impassable = True
        self.flag = 'decor'
        check_params(self)


class GhostParams:
    def __init__(self) -> None:
        self.sprite = pygame.image.load('res/sprites/pin/base/0.png').convert_alpha()
        self.shift = 0.6
        self.scale = (0.6, 0.6)
        self.side = 30
        self.animation = deque(
            [pygame.image.load(f'res/sprites/pin/anim/{i}.png').convert_alpha() for i in range(8)])
        self.is_destroy = 'immortal'
        self.animation_dist = 800
        self.animation_speed = 10
        self.impassable = True
        self.flag = 'decor'
        check_params(self)


def check_params(obj):
    dict_of_attributes = {'[]': ['animation', 'destroy_animation', 'obj_attack'],
                          'None': ['viewing_angles', 'is_destroy', 'impassable', 'destroy_shift']
                          }
    for val in dict_of_attributes.values():
        for attr in val:
            if not hasattr(obj, attr):
                add_param(dict_of_attributes, obj, attr)


def add_param(dct: dict, obj, attribute: str):
    if attribute in dct['[]']:
        setattr(obj, attribute, [])
    elif attribute in dct['None']:
        setattr(obj, attribute, None)
