from collections import deque
import pygame


class SpriteParams:
    def __init__(self,
                 path: str,
                 has_angles: bool,
                 shift: float,
                 scale: tuple[float, float],
                 side: int,
                 frame_count: int | None,
                 anim_dist: int,
                 anim_speed: int,
                 is_dead: int | str,
                 dead_shift: float,
                 blocked: bool,
                 flag: str,
                 obj_action: list | int = None,
                 base_angles: int = 0) -> None:

        self.path = path
        self.has_angles = has_angles
        self.shift = shift
        self.scale = scale
        self.side = side
        self.frame_count = frame_count
        self.anim_dist = anim_dist
        self.anim_speed = anim_speed
        self.is_dead = is_dead
        self.dead_shift = dead_shift
        self.blocked = blocked
        self.flag = flag
        self.obj_action = obj_action
        self.base_angles = base_angles

        self.sprite_name = self.path.split('/')[-3]
        if self.path.split('/')[-4] == 'npc':
            self.sprite_name = 'npc/' + self.sprite_name

        self.sprite = pygame.image.load(self.path).convert_alpha()

        self.death_animation = deque(
            [pygame.image.load(
                f'res/sprites/{self.sprite_name}/death/{i}.png').convert_alpha()
                for i in range(self.is_dead + 1)])if type(self.is_dead) is int else []

        self.obj_action = deque(
            [pygame.image.load(
                f'res/sprites/{self.sprite_name}/anim/{i}.png').convert_alpha() \
             for i in range(self.obj_action + 1)]) if self.obj_action else []

        self.actualFrames = deque(
            [pygame.image.load(
                f'res/sprites/{self.sprite_name}/anim/{i}.png').convert_alpha()
             for i in range(self.frame_count + 1)]) if self.frame_count else []

        if self.has_angles:
            path = self.path[:-5]
            self.sprite = [pygame.image.load(
                f'{path}{i}.png').convert_alpha() for i in range(self.base_angles + 1)]
            self.sprite_angles = [frozenset(range(338, 361)) | frozenset(range(0, 23))] + \
                                 [frozenset(range(i, i + 45)) for i in range(0, 360, 45)]
            self.sprite_positions = {angle: pos for angle, pos in zip(self.sprite_angles, self.sprite)}

        self.npc_action_trigger = False
        self.dead_animation_count = 0
        self.animation_count = 0
        self.side = 30
        self.x, self.y = 0, 0
