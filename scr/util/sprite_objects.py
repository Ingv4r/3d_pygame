import pygame
from util.settings import *
from collections import deque


class SpriteParams:
    def __init__(self,
                 path: str,
                 has_angles: bool,
                 shift: float,
                 scale: float,
                 frames: int | None,
                 anim_dist: int,
                 anim_speed: int,
                 blocked: bool,
                 base_angles: int = 0) -> None:
        self.path = path
        self.has_angles = has_angles
        self.shift = shift
        self.scale = scale
        self.frames = frames
        self.anim_dist = anim_dist
        self.anim_speed = anim_speed
        self.blocked = blocked
        self.base_angles = base_angles

        self.sprite_name = self.path.split('/')[-3]

    def change_sprite(self, dict: dict):
        path = self.path[:-5]
        dict['sprite'] = [pygame.image.load(
            f'{path}{i}.png').convert_alpha() for i in range(self.base_angles+1)]

    def make_dict(self) -> dict:
        dict_of_params = {
            'sprite': pygame.image.load(self.path).convert_alpha(),
            'viewing_angles': self.has_angles,
            'shift': self.shift,
            'scale': self.scale,
            'frames': deque(
                [pygame.image.load(
                    f'res/sprites/{self.sprite_name}/anim/{i}.png').convert_alpha() for i in range(self.frames+1)]
            ) if self.frames else None,
            'animation_dist': self.anim_dist,
            'animation_speed': self.anim_speed,
            'blocked': self.blocked
        }
        if self.base_angles:
            self.change_sprite(dict_of_params)
            
        return dict_of_params


class Sprites():
    def __init__(self):
        root = 'res/sprites/'
        self.sprite_param = {
            'sprite_barrel': SpriteParams.make_dict(
                path=f'{root}barel/base/0.png',
                has_angles=False,
                shift=1.8,
                scale=0.4,
                frames=12,
                anim_dist=800,
                anim_speed=10,
                blocked=True),
            'cacodemon': SpriteParams.make_dict(
                path=f'{root}cacodemon/base/0.png',
                has_angles=True,
                shift=-0.2,
                scale=1.1,
                frames=8,
                anim_dist=700,
                anim_speed=12,
                blocked=True,
                base_angles=7),
            'flame': SpriteParams.make_dict(
                path=f'{root}flame/base/0.png', 
                has_angles=False, 
                shift=1.8, 
                scale=0.4, 
                frames=15, 
                anim_dist=1000, 
                anim_speed=9, 
                blocked=False),
            'pedistal': SpriteParams.make_dict(
                path=f'{root}pedistal/base/0.png', 
                has_angles=False, 
                shift=1.8, 
                scale=0.4, 
                frames=None, 
                anim_dist=800, 
                anim_speed=10, 
                blocked=True),
            'pin': SpriteParams.make_dict(
                f'{root}pin/base/0.png', False, 1.8, 0.4, 7, 800, 5, True),
        }
        self.list_of_objects = [
            SpriteObject(
                self.sprite_param['sprite_barrel'], position=(4.5, 4.5)),
            SpriteObject(
                self.sprite_param['sprite_barrel'], position=(7.5, 4.5)),
            SpriteObject(
                self.sprite_param['cacodemon'], position=(12.5, 11.5)),
            SpriteObject(self.sprite_param['flame'], position=(9, 13.5)),
            SpriteObject(self.sprite_param['flame'], position=(15, 13.5)),
            SpriteObject(self.sprite_param['pedistal'], position=(8, 13.5)),
            SpriteObject(self.sprite_param['pedistal'], position=(16, 13.5)),
            SpriteObject(self.sprite_param['pin'], position=(10.5, 14.5)),
            SpriteObject(self.sprite_param['pin'], position=(13.5, 14.5)),
        ]
        self.collision_sprites = [pygame.Rect(*obj.pos, obj.side, obj.side) for obj in
                                  self.list_of_objects if obj.blocked]


class SpriteObject:
    def __init__(self, parameters, position):
        self.object = parameters['sprite']
        self.viewing_angles = parameters['viewing_angles']
        self.shift = parameters['shift']
        self.scale = parameters['scale']
        self.animation = parameters['animation'].copy(
        ) if parameters['animation'] else None
        self.animation_dist = parameters['animation_dist']
        self.animation_speed = parameters['animation_speed']
        self.animation_count = 0
        self.blocked = parameters['blocked']
        self.side = 30
        self.x, self.y = position[0] * TILE, position[1] * TILE
        self.position = self.x - self.side // 2, self.y - self.side // 2
        if self.viewing_angles:
            self.sprite_angles = [frozenset(range(i, i + 45))
                                  for i in range(0, 360, 45)]
            self.sprite_positions = {angle: pos for angle,
                                     pos in zip(self.sprite_angles, self.object)}

    def object_locate(self, player):

        dx, dy = self.x - player.x, self.y - player.y
        distance_to_sprite = math.sqrt(dx ** 2 + dy ** 2)

        theta = math.atan2(dy, dx)
        gamma = theta - player.angle
        if dx > 0 and 180 <= math.degrees(player.angle) <= 360 or dx < 0 and dy < 0:
            gamma += DOUBLE_PI

        delta_rays = int(gamma / DELTA_ANGLE)
        current_ray = CENTER_RAY + delta_rays
        distance_to_sprite *= math.cos(HALF_FOV - current_ray * DELTA_ANGLE)

        fake_ray = current_ray + FAKE_RAYS
        if 0 <= fake_ray <= FAKE_RAYS_RANGE and distance_to_sprite > 30:
            proj_height = min(
                int(PROJ_COEF / distance_to_sprite * self.scale), DOUBLE_HEIGHT)
            half_proj_height = proj_height // 2
            shift = half_proj_height * self.shift
            # choosing sprite for angle
            if self.viewing_angles:
                if theta < 0:
                    theta += DOUBLE_PI
                theta = 360 - int(math.degrees(theta))

                for angles in self.sprite_angles:
                    if theta in angles:
                        self.object = self.sprite_positions[angles]
                        break

            # sprite animation
            sprite_object = self.object
            if self.animation and distance_to_sprite < self.animation_dist:
                sprite_object = self.animation[0]
                if self.animation_count < self.animation_speed:
                    self.animation_count += 1
                else:
                    self.animation.rotate()
                    self.animation_count = 0

            # sprite scale and pos
            sprite_pos = (current_ray * SCALE - half_proj_height,
                          HALF_HEIGHT - half_proj_height + shift)
            sprite = pygame.transform.scale(
                sprite_object, (proj_height, proj_height))
            return (distance_to_sprite, sprite, sprite_pos)
        else:
            return (False,)
