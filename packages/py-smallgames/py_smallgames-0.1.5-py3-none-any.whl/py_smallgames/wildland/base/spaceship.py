import random
from typing import List

import pygame as pg
from base.sprite import Sprite
from base.constant import SCREEN_RECT


class Alien(pg.sprite.Sprite):
    """An alien space ship. That slowly moves down the screen."""

    speed = 13
    animcycle = 12
    images: List[pg.Surface] = []

    def __init__(self, *groups):
        pg.sprite.Sprite.__init__(self, *groups)
        self.image = self.images[0]
        self.rect = self.image.get_rect()
        self.facing = random.choice((-1, 1)) * Alien.speed
        self.frame = 0
        if self.facing < 0:
            self.rect.right = SCREEN_RECT.right

    def update(self):
        self.rect.move_ip(self.facing, 0)
        if not SCREEN_RECT.contains(self.rect):
            self.facing = -self.facing
            self.rect.top = self.rect.bottom + 1
            self.rect = self.rect.clamp(SCREEN_RECT)
        self.frame = self.frame + 1
        self.image = self.images[self.frame // self.animcycle % 3]
