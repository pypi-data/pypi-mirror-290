import pygame

from . import constants as c
from . import tools

pygame.init()
pygame.display.set_mode(c.WINDOW_SIZE, pygame.SRCALPHA, 32)

GRAPHICS = tools.load_graphic('resources/graphics')
