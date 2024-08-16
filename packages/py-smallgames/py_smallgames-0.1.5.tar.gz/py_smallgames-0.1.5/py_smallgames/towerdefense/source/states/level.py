import pygame

from .state import State
from .. import constants as c
from ..components.map import Map


class LevelState(State):
    def __init__(self):
        State.__init__(self)

        self.next = c.STATE_END

        self.map = Map(map_id=1)
        self.components = pygame.sprite.LayeredUpdates(self.map)

    def update(self, screen: pygame.Surface):
        screen.fill((0, 255, 255))

        self.components.update()
        self.components.draw(screen)

    def handle_key_down(self, key):
        if key == pygame.K_ESCAPE:
            self.finished = True
