import pygame
from util.settings import *
from collections import deque


class SpritesParamsArgs:
    def __init__(self, path, has_angles, shift, scale, frames, anim_dist, anim_speed, blocked, base_angles=0) -> None:
        self.path = path
        self.has_angles = has_angles
        self.shift = shift
        self.scale = scale
        self.frames = frames
        self.anim_dist = anim_dist
        self.anim_speed = anim_speed
        self.blocked = blocked
        self.base_angles = base_angles

    def get_sprite_name(self) -> str:
        return self.path.split('/')[-3]


def make_sprite_params(sp_params: SpritesParamsArgs) -> dict:

    dict_of_params = {
        'sprite': pygame.image.load(sp_params.path).convert_alpha(),
        'viewing_angles': sp_params.has_angles,
        'shift': sp_params.shift,  # 1,8
        'scale': sp_params.scale,  # 0.4
        'animation': deque(
            [pygame.image.load(
                f'res/sprites/{sp_params.get_sprite_name()}/anim/{i}.png').convert_alpha() for i in range(sp_params.frames+1)]
        ) if sp_params.frames else None,
        'animation_dist': sp_params.anim_dist,  # 800
        'animation_speed': sp_params.anim_speed,  # 10
        'blocked': sp_params.blocked
    }
    if sp_params.base_angles:
        path = sp_params.path[:-5]
        dict_of_params['sprite'] = [pygame.image.load(
            f'{path}{i}.png').convert_alpha() for i in range(sp_params.base_angles+1)]
    return dict_of_params


class Sprites():
    def __init__(self):
        self.root = 'res/sprites/'
        self.sprite_param = {
            'sprite_barrel': make_sprite_params(SpritesParamsArgs(
                path=f'{self.root}barel/base/0.png', 
                has_angles=False, 
                shift=1.8, 
                scale=0.4, 
                frames=12, 
                anim_dist=800, 
                anim_speed=10, 
                blocked=True)),
            'cacodemon': make_sprite_params(SpritesParamsArgs(
                path=f'{self.root}cacodemon/base/0.png', 
                has_angles=True, 
                shift=-0.2, 
                scale=1.1, 
                frames=8, 
                anim_dist=700, 
                anim_speed=12,
                blocked=True, 
                base_angles=7)),
            'flame': make_sprite_params(SpritesParamsArgs(
                f'{self.root}flame/base/0.png', False, 1.8, 0.4, 15, 1000, 9, False)),
            'pedistal': make_sprite_params(SpritesParamsArgs( 
                f'{self.root}pedistal/base/0.png', False, 1.8, 0.4, None, 800, 10, True)),
            'pin': make_sprite_params(SpritesParamsArgs(
                f'{self.root}pin/base/0.png', False, 1.8, 0.4, 7, 800, 5, True)),
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
        self.collision_sprites = [pygame.Rect(*obj.pos, obj.side, obj.side) for obj in
                                  self.list_of_objects if obj.blocked]


class SpriteObject:
    def __init__(self, parameters, pos):
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
        self.x, self.y = pos[0] * TILE, pos[1] * TILE
        self.pos = self.x - self.side // 2, self.y - self.side // 2
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
