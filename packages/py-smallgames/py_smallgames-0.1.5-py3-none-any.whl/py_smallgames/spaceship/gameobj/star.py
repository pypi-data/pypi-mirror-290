import random

import pygame


class Star(pygame.sprite.Sprite):
    def __init__(self, size):
        pygame.sprite.Sprite.__init__(self)

        self.image = pygame.Surface([1, 1])

        self.rect = self.image.get_rect()
        self.rect = self.rect.move([random.randint(0, size[0]), random.randint(0, size[1])])

        self.size = size

        self.move = random.randint(5, 25)
        self.current = self.move

    def update(self, screen):
        self.current -= 1
        if self.current == 0:
            self.current = self.move
            self.rect = self.rect.move(-1, 0)

        self.brightness = random.randint(100 - self.move * 4, 255 - self.move * 4)
        self.image.fill([self.brightness, self.brightness, self.brightness])

        if self.rect.right < 0:
            self.rect = self.rect.move(self.size[0], 0)

        screen.blit(self.image, self.rect)
