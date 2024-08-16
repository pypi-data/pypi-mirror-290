import pygame

from .state import State
from .. import constants as c


class EndState(State):
    def __init__(self):
        State.__init__(self)

        self.next = c.STATE_START

    def update(self, screen: pygame.Surface):
        screen.fill((0, 255, 0))

    def handle_key_down(self, key):
        if key == pygame.K_ESCAPE:
            self.finished = True
