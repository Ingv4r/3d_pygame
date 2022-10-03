import uuid
import pygame
from sprite.sprite import Sprite
from util.point2d import Point2d
from util.position import Position
from util.settings import *


class GameObject:

    def __init__(
        self,
        sprite: Sprite,
        position: Position = Position(Point2d()),
        tag: str = ""
    ) -> None:
        self.id: uuid.UUID = uuid.uuid4()
        self.sprite = sprite
        self.position = position
        self.tag = tag

    def update_position(self, position: Position) -> None:
        x = position.point.x * TILE
        y = position.point.y * TILE
        self.position = Position(Point2d(x, y))

    def object_locate(self, player):
        dx = self.position.point.x - player.x
        dy = self.position.point.y - player.y
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
                int(PROJ_COEF / distance_to_sprite * self.sprite.sprite_params.scale), DOUBLE_HEIGHT)
            half_proj_height = proj_height // 2
            shift = half_proj_height * self.sprite.sprite_params.shift
            # choosing sprite for angle
            if self.sprite.sprite_params.has_angles:
                if theta < 0:
                    theta += DOUBLE_PI
                theta = 360 - int(math.degrees(theta))

                for angles in self.sprite.sprite_angles:
                    if theta in angles:
                        self.sprite.sprite = self.sprite.sprite_positions[angles]
                        break

            # sprite animation
            sprite_object = self.sprite.sprite
            if self.sprite.sprite_params.actualFrames and distance_to_sprite < self.sprite.sprite_params.anim_dist:
                sprite_object = self.sprite.sprite_params.actualFrames[0]
                if self.sprite.animation_count < self.sprite.sprite_params.anim_speed:
                    self.sprite.animation_count += 1
                else:
                    self.sprite.sprite_params.actualFrames.rotate()
                    self.sprite.animation_count = 0

            # sprite scale and pos
            sprite_pos = (current_ray * SCALE - half_proj_height,
                          HALF_HEIGHT - half_proj_height + shift)
            sprite = pygame.transform.scale(
                sprite_object, (proj_height, proj_height))
            return distance_to_sprite, sprite, sprite_pos
        else:
            return False,
