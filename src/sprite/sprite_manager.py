from typing import Dict

from sprite.sprite import Sprite
from sprite.sprite_params import SpriteParams


class SpriteManager():
    root_directory = 'res/sprites'
    
    BARREL = "barrel"
    CACODEMON = "cacodemon"
    FLAME = "flame"
    PEDISTAL = "pedistal"

    def __init__(self) -> None:
        self.sprites: Dict[str, Sprite] = dict()

        self.add_sprite(
            SpriteManager.BARREL,
            SpriteParams(
                path=f'{SpriteManager.root_directory}/barel/base/0.png',
                has_angles=False,
                shift=1.8,
                scale=0.4,
                frame_count=12,
                anim_dist=800,
                anim_speed=10,
                blocked=True
            )
        )

        self.add_sprite(
            SpriteManager.CACODEMON,
            SpriteParams(
                path=f'{SpriteManager.root_directory}/cacodemon/base/0.png',
                has_angles=True,
                shift=-0.2,
                scale=1.1,
                frame_count=8,
                anim_dist=700,
                anim_speed=12,
                blocked=True,
                base_angles=7
            )
        )

        self.add_sprite(
            SpriteManager.FLAME,
            SpriteParams(
                path=f'{SpriteManager.root_directory}/flame/base/0.png',
                has_angles=False,
                shift=1.8,
                scale=0.4,
                frame_count=15,
                anim_dist=1000,
                anim_speed=9,
                blocked=False
            )
        )

        self.add_sprite(
            SpriteManager.PEDISTAL,
            SpriteParams(
                path=f'{SpriteManager.root_directory}/pedistal/base/0.png',
                has_angles=False,
                shift=1.8,
                scale=0.4,
                frame_count=None,
                anim_dist=800,
                anim_speed=10,
                blocked=True,
            )
        )

    def add_sprite(self, name: str, sprite_params: SpriteParams) -> Sprite:
        sprite_object = Sprite(sprite_params)
        self.sprites.update({name: sprite_object})
        return sprite_object

    def get_sprite(self, name: str) -> Sprite:
        return self.sprites[name]

    def is_sprite_exists(self, name: str) -> bool:
        return self.sprites[name] is Sprite
