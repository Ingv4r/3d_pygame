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

        if type(self.is_dead) is int:
            self.death_animation = deque(
                [pygame.image.load(
                    f'res/sprites/{self.sprite_name}/death/{i}.png').convert_alpha()
                 for i in range(self.is_dead + 1)]
                )

        if self.obj_action:
            self.obj_action = deque(
                [pygame.image.load(
                    f'res/sprites/{self.sprite_name}/anim/{i}.png').convert_alpha()
                 for i in range(self.obj_action + 1)]
                )

        self.actualFrames = deque(
            [pygame.image.load(
                f'res/sprites/{self.sprite_name}/anim/{i}.png').convert_alpha()
             for i in range(self.frame_count + 1)]) if self.frame_count else None
