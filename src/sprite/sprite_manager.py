from typing import Dict
from sprite.sprite_params import SpriteParams


class SpriteManager:
    root_directory = 'res/sprites'
    
    BARREL = "barrel"
    CACODEMON = "cacodemon"
    FLAME = "flame"
    PEDISTAL = "pedistal"

    def __init__(self) -> None:
        self.sprites: Dict[str, SpriteParams] = dict()

        self.add_sprite(
            SpriteManager.BARREL,
            SpriteParams(
                path=f'{SpriteManager.root_directory}/barrel/base/0.png',
                has_angles=False,
                shift=1.8,
                scale=(0.4, 0.4),
                side=30,
                frame_count=12,
                anim_dist=800,
                anim_speed=10,
                is_dead=3,
                dead_shift=2.6,
                blocked=True,
                flag='decor',
                obj_action=[]
            )
        )

        self.add_sprite(
            SpriteManager.CACODEMON,
            SpriteParams(
                path=f'{SpriteManager.root_directory}/npc/cacodemon/base/0.png',
                has_angles=True,
                shift=0.0,
                scale=(1.1, 1.1),
                side=50,
                frame_count=8,
                anim_dist=700,
                anim_speed=12,
                is_dead=5,
                dead_shift=0.6,
                blocked=True,
                flag='npc',
                obj_action=8,
                base_angles=7
            )
        )

        self.add_sprite(
            SpriteManager.FLAME,
            SpriteParams(
                path=f'{SpriteManager.root_directory}/flame/base/0.png',
                has_angles=False,
                shift=1.7,
                scale=(0.6, 0.6),
                side=30,
                frame_count=15,
                anim_dist=1000,
                anim_speed=9,
                is_dead='immortal',
                dead_shift=0.0,
                blocked=False,
                flag='decor',
            )
        )

        self.add_sprite(
            SpriteManager.PEDISTAL,
            SpriteParams(
                path=f'{SpriteManager.root_directory}/pedestal/base/0.png',
                has_angles=False,
                shift=1.8,
                scale=(0.4, 0.4),
                side=30,
                frame_count=None,
                anim_dist=800,
                anim_speed=10,
                is_dead='immortal',
                dead_shift=0.0,
                blocked=True,
                flag='decor'
            )
        )

    def add_sprite(self, name: str, sprite_params: SpriteParams) -> SpriteParams:
        sprite_object = sprite_params
        self.sprites.update({name: sprite_object})
        return sprite_object

    def get_sprite(self, name: str) -> SpriteParams:
        return self.sprites[name]

