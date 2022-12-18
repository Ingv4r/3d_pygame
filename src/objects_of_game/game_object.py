from src.util.settings import *
from src.util.position import Position, Point2d
from src.objects_of_game.ojects_parameters import *
import pygame


class GameObject:
    def __init__(self,
                 parameters: BarrelParams |
                             FlameParams |
                             CacodemonParams |
                             PedestalParams |
                             GhostParams |
                             DoorVParams |
                             DoorHParams,
                 pos: tuple) -> None:
        self.sprite = parameters.sprite.copy()
        self.viewing_angles = parameters.viewing_angles
        self.shift = parameters.shift
        self.scale = parameters.scale
        self.animation = parameters.animation.copy()
        # ---------------------
        self.destroy_animation = parameters.destroy_animation.copy()
        self.is_destroy = parameters.is_destroy
        self.destroy_shift = parameters.destroy_shift
        # ---------------------
        self.animation_dist = parameters.animation_dist
        self.animation_speed = parameters.animation_speed
        self.impassable = parameters.impassable
        self.flag = parameters.flag
        self.obj_attack = parameters.obj_attack.copy()
        self.x, self.y = pos[0] * TILE, pos[1] * TILE
        self.side = parameters.side
        self.destroy_anim_count = 0
        self.animation_count = 0
        self.npc_action_trigger = False
        self.door_open_trigger = False
        self.door_prev_pos = self.y if self.flag == 'door_h' else self.x
        self.delete = False
        if self.viewing_angles:
            self.sprite_angles = parameters.sprite_angles
            self.sprite_positions = {angle: pos for angle, pos in zip(self.sprite_angles, self.sprite)}
        # Parameters to calculate. Initialized here for ease of calling inside class methods
        self.distance_to_sprite = None
        self.theta = None
        self.current_ray = None
        self.proj_height = None
        self.destroy_sprite = None

    @property
    def is_on_fire(self):
        if CENTER_RAY - self.side // 2 < self.current_ray < CENTER_RAY + self.side // 2 and self.impassable:
            return self.distance_to_sprite, self.proj_height
        return float('inf'), None

    @property
    def pos(self):
        return self.x - self.side // 2, \
               self.y - self.side // 2

    '''def update_position(self, position: Position) -> None:
        self.x = position.point.x * TILE
        self.y = position.point.y * TILE
        self.position = Position(Point2d(self.x, self.y))'''

    def object_calculations(self, player):
        dx = self.x - player.x
        dy = self.y - player.y
        self.distance_to_sprite = math.sqrt(dx ** 2 + dy ** 2)

        self.theta = math.atan2(dy, dx)
        gamma = self.theta - player.angle
        if dx > 0 and 180 <= math.degrees(player.angle) <= 360 or dx < 0 and dy < 0:
            gamma += DOUBLE_PI
        self.theta -= 1.4 * gamma

        delta_rays = int(gamma / DELTA_ANGLE)
        self.current_ray = CENTER_RAY + delta_rays
        if self.flag not in ['door_v', 'door_h']:
            self.distance_to_sprite *= math.cos(HALF_FOV - self.current_ray * DELTA_ANGLE)

        fake_ray = self.current_ray + FAKE_RAYS
        return fake_ray

    def object_locate(self, player):
        fake_ray = self.object_calculations(player)

        if 0 <= fake_ray <= FAKE_RAYS_RANGE and self.distance_to_sprite > 30:
            self.proj_height = min(
                int(PROJ_COEF / self.distance_to_sprite), DOUBLE_HEIGHT
                if self.flag not in ['door_v', 'door_h']
                else HEIGHT)
            sprite_width = int(self.proj_height * self.scale[0])
            sprite_height = int(self.proj_height * self.scale[1])
            half_sprite_width = sprite_width // 2
            half_sprite_height = sprite_height // 2
            shift = half_sprite_height * self.shift

            # logic for doors
            if self.flag in ['door_v', 'door_h']:
                if self.door_open_trigger:
                    self.open_doors()
                self.sprite = self.visible_sprite()
                sprite_object = self.object_animation()
            else:
                if self.is_destroy and self.is_destroy != 'immortal':
                    sprite_object = self.destroy_anim()
                    shift = half_sprite_height + self.destroy_shift
                    sprite_height = int(sprite_height / 1.3)
                elif self.npc_action_trigger:
                    sprite_object = self.npc_attack()
                else:
                    self.sprite = self.visible_sprite()
                    sprite_object = self.object_animation()

            # Objects_of_game scale and pos
            sprite_pos = (self.current_ray * SCALE - half_sprite_width,
                          HALF_HEIGHT - half_sprite_height + shift)
            sprite = pygame.transform.scale(
                sprite_object, (sprite_width, sprite_height))
            return self.distance_to_sprite, sprite, sprite_pos
        else:
            return False,

    def object_animation(self):
        if self.animation and self.distance_to_sprite < self.animation_dist:
            sprite_object = self.animation[0]
            if self.animation_count < self.animation_speed:
                self.animation_count += 1
            else:
                self.animation.rotate()
                self.animation_count = 0
            return sprite_object
        return self.sprite

    def visible_sprite(self):
        if self.viewing_angles:
            if self.theta < 0:
                self.theta += DOUBLE_PI
            self.theta = 360 - int(math.degrees(self.theta))

            for angles in self.sprite_angles:
                if self.theta in angles:
                    return self.sprite_positions[angles]
        return self.sprite

    def destroy_anim(self):
        if len(self.destroy_animation):
            if self.destroy_anim_count < self.animation_speed:
                self.destroy_sprite = self.destroy_animation[0]
                self.destroy_anim_count += 1
            else:
                self.destroy_sprite = self.destroy_animation.popleft()
                self.destroy_anim_count = 0
        else:
            self.delete = True
        return self.destroy_sprite

    def npc_attack(self):
        sprite_object = self.obj_attack[0]
        if self.animation_count < self.animation_speed:
            self.animation_count += 1
        else:
            self.obj_attack.rotate()
            self.animation_count = 0
        return sprite_object

    def open_doors(self):
        if self.flag == 'door_h':
            self.y -= 3
            if abs(self.y - self.door_prev_pos) > TILE:
                self.delete = True
        elif self.flag == 'door_v':
            self.x -= 3
            if abs(self.x - self.door_prev_pos) > TILE:
                self.delete = True
