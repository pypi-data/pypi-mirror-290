import pygame

from .. import setup


class Button(pygame.sprite.Sprite):
    """按钮精灵，参数：
    pos(x,y)：初始位置
    images:鼠标hover前后的图片"""

    def __init__(self, pos: tuple, images: tuple):
        pygame.sprite.Sprite.__init__(self)

        self.images = [setup.GRAPHICS[img] for img in images]
        self.image = self.images[0]
        self.rect = self.image.get_rect()
        self.rect.center = pos

    def update(self):
        mouse_pos = pygame.mouse.get_pos()
        if self.rect.collidepoint(mouse_pos):
            self.image = self.images[1]
        else:
            self.image = self.images[0]
