import uuid
import pygame
from util.settings import *
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

    @property
    def is_on_fire(self):
        if CENTER_RAY - self.sprite.sprite_params.side // 2 < \
                self.current_ray < \
                CENTER_RAY + self.sprite.sprite_params.side // 2 and \
                self.sprite.sprite_params.blocked:
            return self.distance_to_sprite, self.proj_height
        return float('inf'), None

    @property
    def pos(self):
        return self.x - self.sprite.sprite_params.side // 2, \
               self.y - self.sprite.sprite_params.side // 2

    def update_position(self, position: Position) -> None:
        self.x = position.point.x * TILE
        self.y = position.point.y * TILE
        self.position = Position(Point2d(self.x, self.y))

    def object_locate(self, player):
        dx = self.position.point.x - player.x
        dy = self.position.point.y - player.y
        distance_to_sprite = math.sqrt(dx ** 2 + dy ** 2)

        self.theta = math.atan2(dy, dx)
        gamma = self.theta - player.angle
        if dx > 0 and 180 <= math.degrees(player.angle) <= 360 or dx < 0 and dy < 0:
            gamma += DOUBLE_PI

        delta_rays = int(gamma / DELTA_ANGLE)
        self.current_ray = CENTER_RAY + delta_rays
        distance_to_sprite *= math.cos(HALF_FOV - self.current_ray * DELTA_ANGLE)

        fake_ray = self.current_ray + FAKE_RAYS
        self.distance_to_sprite = distance_to_sprite
        if 0 <= fake_ray <= FAKE_RAYS_RANGE and self.distance_to_sprite > 30:
            proj_height = min(
                int(PROJ_COEF / self.distance_to_sprite * self.sprite.sprite_params.scale), DOUBLE_HEIGHT)
            self.proj_height = proj_height
            half_proj_height = self.proj_height // 2
            shift = half_proj_height * self.sprite.sprite_params.shift
            # choosing sprite for angle
            if self.sprite.sprite_params.has_angles:
                if self.theta < 0:
                    self.theta += DOUBLE_PI
                self.theta = 360 - int(math.degrees(self.theta))

                for angles in self.sprite.sprite_angles:
                    if self.theta in angles:
                        self.sprite.sprite = self.sprite.sprite_positions[angles]
                        break

            # sprite animation
            sprite_object = self.sprite.sprite
            if self.sprite.sprite_params.actualFrames and self.distance_to_sprite < self.sprite.sprite_params.anim_dist:
                sprite_object = self.sprite.sprite_params.actualFrames[0]
                if self.sprite.animation_count < self.sprite.sprite_params.anim_speed:
                    self.sprite.animation_count += 1
                else:
                    self.sprite.sprite_params.actualFrames.rotate()
                    self.sprite.animation_count = 0

            # sprite scale and pos
            sprite_pos = (self.current_ray * SCALE - half_proj_height,
                          HALF_HEIGHT - half_proj_height + shift)
            sprite = pygame.transform.scale(
                sprite_object, (self.proj_height, self.proj_height))
            return self.distance_to_sprite, sprite, sprite_pos
        else:
            return False,
