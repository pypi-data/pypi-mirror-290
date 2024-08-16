import sys

import pygame

from .state import State
from .. import constants as c
from ..components.background import Background
from ..components.button import Button


class StartState(State):
    def __init__(self):
        State.__init__(self)

        self.next = c.STATE_LEVEL

        self.pb_play = Button(pos=(400, 400), images=('play_black', 'play_red'))
        self.pb_quit = Button(pos=(400, 480), images=('quit_black', 'quit_red'))
        self.background_img = Background('start_interface', c.WINDOW_W, c.WINDOW_H)
        self.components = pygame.sprite.LayeredUpdates(self.background_img, self.pb_play, self.pb_quit)

    def update(self, screen: pygame.Surface):
        self.components.update()
        self.components.draw(screen)

    def handle_mouse_down(self, button: int):
        if button == 1:
            mouse_pos = pygame.mouse.get_pos()
            if self.pb_play.rect.collidepoint(mouse_pos):
                self.finished = True
            if self.pb_quit.rect.collidepoint(mouse_pos):
                pygame.quit()
                sys.exit(0)

    def handle_key_down(self, key):
        pass
