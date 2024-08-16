import sys

import pygame

from . import constants as c


class Game:
    def __init__(self, state_dict: dict, start_state: int):
        self.screen = pygame.display.get_surface()
        self.clock = pygame.time.Clock()
        self.running = True

        self.state_dict = state_dict
        self.state = self.state_dict[start_state]

    def update(self):
        if self.state.finished:
            next_state = self.state.next
            self.state.finished = False
            self.state = self.state_dict[next_state]

        self.state.update(self.screen)
        pygame.display.update()

    def run(self):
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit(0)
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    self.state.handle_mouse_down(event.button)
                elif event.type == pygame.KEYDOWN:
                    self.state.handle_key_down(event.key)

            self.update()
            self.clock.tick(c.GAME_FPS)
