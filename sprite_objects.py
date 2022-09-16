from multiprocessing.sharedctypes import Value
import pygame
from settings import *
from collections import deque

def make_sprite_params(
                        sprite_name: str, sprite_path: str,  viewing_angles: bool, shift: int, scale: int, 
                        frames: int | None, animation_dist: int, animation_speed: int, base_angles=0,
                        ) -> dict:
        dict = {
            'sprite': pygame.image.load(sprite_path).convert_alpha(),
            'viewing_angles': viewing_angles,
            'shift': shift, # 1,8
            'scale': scale, # 0.4
            'animation': deque([pygame.image.load(f'sprites/{sprite_name}/anim/{i}.png').convert_alpha() for i in range(frames+1)]) if frames else None,
            'animation_dist': animation_dist, # 800
            'animation_speed': animation_speed, # 10
            }    
        if base_angles:
            path = sprite_path[:-5]
            dict['sprite'] = [pygame.image.load(f'{path}{i}.png').convert_alpha() for i in range(base_angles+1)]
        return dict

class Sprites():
    def __init__(self):
        self.sprite_param = {
            'sprite_barrel': make_sprite_params('barel', 'sprites/barel/base/0.png', False, 1.8, 0.4, 12, 800, 10),
            'cacodemon': make_sprite_params('cacodemon', 'sprites/cacodemon/base/0.png', True, -0.2, 1.1, 8, 800, 12, 7),
            'flame': make_sprite_params('flame', 'sprites/flame/base/0.png', False, 1.8, 0.4, 15, 800, 9),
            'pedistal': make_sprite_params('pedistal', 'sprites/pedistal/base/0.png', False, 1.8, 0.4, None, 800, 10),
            'pin': make_sprite_params('pin', 'sprites/pin/base/0.png', False, 1.8, 0.4, 7, 800, 6),
        }
        self.list_of_objects = [
            SpriteObject(self.sprite_param['sprite_barrel'], (4.5, 4.5)),
            SpriteObject(self.sprite_param['sprite_barrel'], (7.5, 4.5)),
            SpriteObject(self.sprite_param['cacodemon'], (12.5, 11.5)),
            SpriteObject(self.sprite_param['flame'], (9, 13.5)),
            SpriteObject(self.sprite_param['flame'], (15, 13.5)),
            SpriteObject(self.sprite_param['pedistal'], (8, 13.5)),
            SpriteObject(self.sprite_param['pedistal'], (16, 13.5)),
            SpriteObject(self.sprite_param['pin'], (10.5, 14.5)),
            SpriteObject(self.sprite_param['pin'], (13.5, 14.5)),
        ]

class SpriteObject():
    def __init__(self, param, pos) -> None:
        self.object = param['sprite']
        self.viewing_angles = param['viewing_angles']
        self.shift = param['shift']
        self.scale = param['scale']
        self.animation = param['animation']
        self.animation_dist = param['animation_dist']
        self.animation_speed = param['animation_speed']
        self.animation_count = 0
        self.pos = self.x, self.y = pos[0] * TILE, pos[1] * TILE
        if self.viewing_angles:
            self.sprite_angles = [frozenset(range(i, i + 45)) for i in range(0, 360, 45)]
            self.sprite_position = {angle: pos for angle, pos in zip(self.sprite_angles, self.object)}

    def object_locate(self, player):

        dx, dy = self.x - player.x, self.y - player.y
        distance_to_sprite = math.sqrt(dx ** 2 + dy ** 2)

        theta = math.atan2(dy, dx)
        gamma = theta - player.angle
        if dx > 0 and 180 <= math.degrees(player_angle) <= 360 or dx < 0 and dy < 0:
            gamma = DOUBLE_PI
        
        delta_rays = int(gamma / DELTA_ANGLE)
        current_ray = CENTER_RAY + delta_rays
        distance_to_sprite *= math.cos(HALF_FOV - current_ray * DELTA_ANGLE)

        fake_ray = current_ray + FAKE_RAYS
        if 0 <= fake_ray <= FAKE_RAYS_RANGE and distance_to_sprite > 30:
            proj_height = min(int(PROJ_COEF / distance_to_sprite * self.scale), DOUBLE_HEIGHT)
            half_proj_height = proj_height // 2
            shift = half_proj_height * self.shift
            # chosing sprite for angle
            if self.viewing_angles:
                if theta < 0:
                    theta += DOUBLE_PI
                theta = 360 - int(math.degrees(theta)) 

                for angles in self.sprite_angles:
                    if theta in angles:
                        self.object = self.sprite_position[angles]
                        break

            #sprite animation
            sprite_obj = self.object
            if self.animation and distance_to_sprite < self.animation_dist:
                sprite_obj = self.animation[0]
                if self.animation_count < self.animation_speed:
                    self.animation_count += 1
                else:
                    self.animation.rotate()
                    self.animation_count = 0

            #sprite scale and pos
            sprite_pos = (current_ray * SCALE - half_proj_height, HALF_HEIGHT - half_proj_height + shift)
            sprite = pygame.transform.scale(sprite_obj, (proj_height, proj_height))
            return(distance_to_sprite, sprite, sprite_pos)
        else:
            return (False,)