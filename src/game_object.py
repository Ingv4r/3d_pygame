import pygame
from util.settings import *
from util.point2d import Point2d
from util.position import Position
from sprite.sprite_params import SpriteParams


class GameObject:
    def __init__(
            self,
            sprite: SpriteParams,
            position: Position = Position(Point2d()),
    ) -> None:
        self.sprite = sprite
        self.object = sprite.sprite.copy()
        self.animation = sprite.actualFrames.copy()
        self.death_animation = sprite.death_animation.copy()
        self.obj_action = sprite.obj_action.copy()
        self.position = position

    @property
    def is_on_fire(self):
        if CENTER_RAY - self.sprite.side // 2 < \
                self.current_ray < \
                CENTER_RAY + self.sprite.side // 2 and \
                self.sprite.blocked:
            return self.distance_to_sprite, self.proj_height
        return float('inf'), None

    @property
    def pos(self):
        return self.x - self.sprite.side // 2, \
               self.y - self.sprite.side // 2

    def update_position(self, position: Position) -> None:
        self.x = position.point.x * TILE
        self.y = position.point.y * TILE
        self.position = Position(Point2d(self.x, self.y))

    def object_locate(self, player):
        dx = self.position.point.x - player.x
        dy = self.position.point.y - player.y
        self.distance_to_sprite = math.sqrt(dx ** 2 + dy ** 2)

        self.theta = math.atan2(dy, dx)
        gamma = self.theta - player.angle
        if dx > 0 and 180 <= math.degrees(player.angle) <= 360 or dx < 0 and dy < 0:
            gamma += DOUBLE_PI
        self.theta -= 1.4 * gamma

        delta_rays = int(gamma / DELTA_ANGLE)
        self.current_ray = CENTER_RAY + delta_rays
        self.distance_to_sprite *= math.cos(HALF_FOV - self.current_ray * DELTA_ANGLE)

        fake_ray = self.current_ray + FAKE_RAYS
        if 0 <= fake_ray <= FAKE_RAYS_RANGE and self.distance_to_sprite > 30:
            self.proj_height = min(
                int(PROJ_COEF / self.distance_to_sprite), DOUBLE_HEIGHT)
            sprite_width = int(self.proj_height * self.sprite.scale[0])
            sprite_height = int(self.proj_height * self.sprite.scale[1])
            half_sprite_width = sprite_width // 2
            half_sprite_height = sprite_height // 2
            shift = half_sprite_height * self.sprite.shift

            if self.sprite.is_dead and self.sprite.is_dead != 'immortal':
                sprite_object = self.death_anim()
                shift = half_sprite_height + self.sprite.dead_shift
                sprite_height = int(sprite_height / 1.3)
            elif self.sprite.npc_action_trigger:
                sprite_object = self.npc_in_action()
            else:
                self.object = self.visible_sprite()
                sprite_object = self.sprite_animation()

            # sprite scale and pos
            sprite_pos = (self.current_ray * SCALE - half_sprite_width,
                          HALF_HEIGHT - half_sprite_height + shift)
            sprite = pygame.transform.scale(
                sprite_object, (sprite_width, sprite_height))
            return self.distance_to_sprite, sprite, sprite_pos
        else:
            return False,

    def sprite_animation(self):
        if self.animation and self.distance_to_sprite < self.sprite.anim_dist:
            sprite_object = self.animation[0]
            if self.sprite.animation_count < self.sprite.anim_speed:
                self.sprite.animation_count += 1
            else:
                self.animation.rotate()
                self.sprite.animation_count = 0
            return sprite_object
        return self.object

    def visible_sprite(self):
        if self.sprite.has_angles:
            if self.theta < 0:
                self.theta += DOUBLE_PI
            self.theta = 360 - int(math.degrees(self.theta))

            for angles in self.sprite.sprite_angles:
                if self.theta in angles:
                    return self.sprite.sprite_positions[angles]
        return self.object

    def death_anim(self):
        if len(self.death_animation):
            if self.sprite.dead_animation_count < self.sprite.anim_speed:
                self.death_sprite = self.sprite.death_animation[0]
                self.sprite.dead_animation_count += 1
            else:
                self.death_sprite = self.death_animation.popleft()
                self.sprite.dead_animation_count = 0
        return self.death_sprite

    def npc_in_action(self):
        sprite_object = self.obj_action[0]
        if self.sprite.animation_count < self.sprite.anim_speed:
            self.sprite.animation_count += 1
        else:
            self.obj_action.rotate()
            self.sprite.animation_count = 0
        return sprite_object


