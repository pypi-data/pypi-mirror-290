import os
from typing import Tuple

import pygame as pg
from base.constant import DIR_ASSETS


def convert_color(x: int) -> Tuple[int, int, int]:
    """转化 hex 格式为 tuple 格式."""
    return (x & 0xFF0000) >> 16, (x & 0xFF00) >> 8, (x & 0xFF)


def load_image(file):
    """loads an image, prepares it for play"""
    file = DIR_ASSETS / "images" / file
    try:
        surface = pg.image.load(str(file))
    except pg.error:
        raise SystemExit(f'Could not load image "{file}" {pg.get_error()}')
    return surface.convert()


def load_sound(file):
    """because pygame can be be compiled without mixer."""
    if not pg.mixer:
        return None
    file = DIR_ASSETS / "music" / file
    try:
        sound = pg.mixer.Sound(str(file))
        return sound
    except pg.error:
        print(f"Warning, unable to load, {file}")
    return None
