from collections import deque
import pygame


class SpriteParams:
    def __init__(self,
                 path: str,
                 has_angles: bool,
                 shift: float,
                 scale: float,
                 frame_count: int | None,
                 anim_dist: int,
                 anim_speed: int,
                 blocked: bool,
                 base_angles: int = 0) -> None:
        self.path = path
        self.has_angles = has_angles
        self.shift = shift
        self.scale = scale
        self.frame_count = frame_count
        self.anim_dist = anim_dist
        self.anim_speed = anim_speed
        self.blocked = blocked
        self.base_angles = base_angles

        self.sprite_name = self.path.split('/')[-3]
        self.actualFrames = deque(
            [pygame.image.load(
                f'res/sprites/{self.sprite_name}/anim/{i}.png').convert_alpha() for i in range(self.frame_count+1)]
        ) if self.frame_count else None
