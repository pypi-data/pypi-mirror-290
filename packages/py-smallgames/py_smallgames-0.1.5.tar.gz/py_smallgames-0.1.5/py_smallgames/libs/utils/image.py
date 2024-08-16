import typing

import pygame
import pygame as pg


def load_image(
    image_path: str,
    color_key: typing.Union[
        int,
        str,
        pg.Color,
        typing.Tuple[int, int, int],
        typing.Tuple[int, int, int, int],
    ] = None,
) -> pg.Surface:
    """Loads an image and returns it."""
    image = pygame.image.load(image_path).convert()
    if color_key is not None:
        image.set_colorkey(color_key)
    return image
