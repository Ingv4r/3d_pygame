from collections import deque
import pygame


class InteractParamsHolder:
    def __init__(self) -> None:
        self.barrel = BarrelParams()
        self.flame = FlameParams()
        self.ghost = GhostParams()
        self.cacodemon = CacodemonParams()
        self.pedestal = PedestalParams()
        self.doorV = DoorVParams()
        self.doorH = DoorHParams()


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
        self.destroy_shift = -10.0
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


class DoorVParams:
    def __init__(self) -> None:
        self.sprite = [pygame.image.load(f'res/sprites/doors/door_v/{i}.png') for i in range(16)]
        self.viewing_angles = True
        self.shift = 0.1
        self.scale = (2.6, 1.2)
        self.side = 100
        self.is_destroy = 'immortal'
        self.impassable = True
        self.flag = 'door_v'
        check_params(self)


class DoorHParams:
    def __init__(self) -> None:
        self.sprite = [pygame.image.load(f'res/sprites/doors/door_h/{i}.png') for i in range(16)]
        self.viewing_angles = True
        self.shift = 0.1
        self.scale = (2.6, 1.2)
        self.side = 100
        self.is_destroy = 'immortal'
        self.impassable = True
        self.flag = 'door_h'
        check_params(self)


def check_params(class_object):
    lost_parameters = {'[]': ['animation', 'destroy_animation', 'obj_attack', 'sprite'],
                       'None': ['viewing_angles', 'impassable', 'destroy_shift'],
                       '0': ['shift', 'side', 'animation_dist', 'animation_speed', 'is_destroy'],
                       '': ['flag']
                       }
    if hasattr(class_object, 'viewing_angles'):
        add_sprite_angles(class_object)

    for val in lost_parameters.values():
        for attr in val:
            if not hasattr(class_object, attr):
                add_param(lost_parameters, class_object, attr)


def add_param(dct: dict, obj, attribute: str):
    if attribute in dct['[]']:
        setattr(obj, attribute, [])
    elif attribute in dct['None']:
        setattr(obj, attribute, None)
    elif attribute in dct['0']:
        setattr(obj, attribute, 0)
    elif attribute in dct['']:
        setattr(obj, attribute, '')


def add_sprite_angles(obj):
    if len(obj.sprite) == 8:
        obj.sprite_angles = [frozenset(range(338, 361)) | frozenset(range(0, 23))] + \
                            [frozenset(range(i, i + 45)) for i in range(23, 338, 45)]
    else:
        obj.sprite_angles = [frozenset(range(348, 361)) | frozenset(range(0, 11))] + \
                            [frozenset(range(i, i + 23)) for i in range(11, 348, 23)]
    obj.sprite_positions = {angle: pos for angle, pos in zip(obj.sprite_angles, obj.sprite)}
