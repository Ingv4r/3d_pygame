from collections import deque
import pygame


def check_attributes(obj: str):
    dict_of_attributes = {'[]': ['animation', 'destroy_animation', 'obj_attack'],
                          'None': ['viewing_angles', 'is_destroy', 'impassable', 'destroy_shift']
                          }
    for val in dict_of_attributes.values():
        for attr in val:
            if not hasattr(obj, attr):
                add_attribute(dict_of_attributes, obj, attr)


def add_attribute(dct: dict, obj: str, attribute: str):
    if attribute in dct['[]']:
        exec(f'{obj}.{attribute} = []')
    elif attribute in dct['None']:
        exec(f'{obj}.{attribute} = None')


def add_required_attributes(game_obj):
    if game_obj.viewing_angles:
        if len(game_obj.sprite) == 8:
            game_obj.sprite_angles = [frozenset(range(338, 361)) | frozenset(range(0, 23))] + \
                                 [frozenset(range(i, i + 45)) for i in range(23, 338, 45)]
        else:
            game_obj.sprite_angles = [frozenset(range(348, 361)) | frozenset(range(0, 11))] + \
                                 [frozenset(range(i, i + 23)) for i in range(11, 348, 23)]

        game_obj.sprite_positions = {angle: pos for angle, pos in zip(game_obj.sprite_angles, game_obj.sprite)}

    game_obj.npc_action_trigger = False
    game_obj.destroy_anim_count = 0
    game_obj.animation_count = 0
    game_obj.x, game_obj.y = 0, 0


class Barrel:
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
        self.destroy_shift = 2.6
        self.animation_dist = 800
        self.animation_speed = 10
        self.impassable = True
        self.flag = 'decor'


class Cacodemon:
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


class Flame:
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


class Pedestal:
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


class Pin:
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


class SpriteManager:
    BARREL = "Barrel"
    CACODEMON = "Cacodemon"
    FLAME = "Flame"
    PEDESTAL = "Pedestal"
    PIN = "Pin"

    def __init__(self) -> None:
        self.sprites: dict = dict()
        barrel, pin, pedestal, cacodemon, flame = Barrel(), Pin(), Pedestal(), Cacodemon(), Flame()
        self.add_sprites(barrel, pin, pedestal, cacodemon, flame)
        print(self.sprites)

    def add_sprites(self, *objects):
        for obj in objects:
            self.sprites.update({type(obj).__name__: obj})

    def get_sprite(self, name: str):
        return self.sprites[name]
