import pygame

from .. import setup


class Background(pygame.sprite.Sprite):
    """背景精灵"""

    def __init__(self, img: str, width: int, height: int):
        super().__init__()

        self.image = setup.GRAPHICS[img]
        self.rect = self.image.get_rect()
        self.rect.center = width / 2, height / 2

    def update(self):
        pass
