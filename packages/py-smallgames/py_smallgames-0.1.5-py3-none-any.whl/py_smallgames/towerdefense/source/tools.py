import os

import pygame


def load_graphic(path: str, allowed_ext=('.jpg', '.png', '.bmp', '.gif')):
    """载入path目录下所有图片文件"""
    graphics = {}
    for picture in os.listdir(path):
        name, ext = os.path.splitext(picture)
        if ext.lower() in allowed_ext:
            img = pygame.image.load(os.path.join(path, picture))
            if img.get_alpha():
                img = img.convert_alpha()
            else:
                img = img.convert()
            graphics[name] = img
    return graphics


def get_image(sheet: pygame.Surface, x: int, y: int, width: int, height: int, colorkey: tuple, scale: float):
    image = pygame.Surface((width, height))
    image.blit(sheet, (0, 0), (x, y, width, height))
    image.set_colorkey(colorkey)
    image = pygame.transform.scale(image, (int(width * scale), (int(height * scale))))
    return image
