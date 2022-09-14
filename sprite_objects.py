import pygame
from settings import *

class Sprites():
    def __init__(self):
        self.sprite_types = {
            'barrel': pygame.image.load('sprites/barel/0.png').convert_alpha(),
            'pedistal': pygame.image.load('sprites/pedistal/0.png').convert_alpha(),
            'cacodemon': [pygame.image.load(f'sprites/cacodemon/{i}.png').convert_alpha() for i in range(8)]
        }
        self.list_of_objects = [
            SpriteObject(self.sprite_types['barrel'], True, (4.5, 4.5), 1.8, 0.4),
            SpriteObject(self.sprite_types['barrel'], True, (7.5, 4.5), 1.8, 0.4),
            SpriteObject(self.sprite_types['pedistal'], True, (4.3, 2.5), 1.6, 0.4),
            SpriteObject(self.sprite_types['pedistal'], True, (7.7, 2.5), 1.6, 0.4),
            SpriteObject(self.sprite_types['cacodemon'], False, (6.5, 3.5), -0.2, 0.7),
        ]

class SpriteObject():
    def __init__(self, object, static, pos, shift, scale) -> None:
        self.object = object
        self.static = static
        self.pos = self.x, self.y = pos[0] * TILE, pos[1] * TILE
        self.shift = shift
        self.scale = scale

        if not static:
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

            if not self.static:
                if theta < 0:
                    theta += DOUBLE_PI
                theta = 360 - int(math.degrees(theta)) 

                for angles in self.sprite_angles:
                    if theta in angles:
                        self.object = self.sprite_position[angles]
                        break


            sprite_pos = (current_ray * SCALE - half_proj_height, HALF_HEIGHT - half_proj_height + shift)
            sprite = pygame.transform.scale(self.object, (proj_height, proj_height))
            return(distance_to_sprite, sprite, sprite_pos)
        else:
            return (False,)