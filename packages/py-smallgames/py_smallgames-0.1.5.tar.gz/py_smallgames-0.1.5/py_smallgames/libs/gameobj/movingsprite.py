import typing

import pygame as pg

from py_smallgames.libs.utils.image import load_image

vec = pg.math.Vector2


class MovingSprite(pg.sprite.Sprite):
    """可移动sprite的基类"""

    IMG = ""

    def __init__(
        self,
        pos: typing.Tuple[int, int],
        vel: typing.Tuple[float, float] = vec(0.0, 0.0),
        acc: typing.Tuple[float, float] = vec(0.0, 0.0),
    ):
        super().__init__()

        self.img = load_image(self.IMG)
        self.rect = self.img.get_rect(x=pos[0], y=pos[1])
        self.vel = vec(vel)
        self.acc = vec(acc)

    def update(self, screen: pg.Surface, time, ship):
        print(self.vel)
        self.rect = self.rect.move(self.vel)
        screen.blit(self.img, self.rect)
