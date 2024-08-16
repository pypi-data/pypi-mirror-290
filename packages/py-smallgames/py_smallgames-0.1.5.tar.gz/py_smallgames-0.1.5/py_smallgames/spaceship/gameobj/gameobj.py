import pygame as pg


class GameObject(pg.sprite.Sprite):
    """所有sprite的基类"""

    def __init__(self):
        super().__init__()

