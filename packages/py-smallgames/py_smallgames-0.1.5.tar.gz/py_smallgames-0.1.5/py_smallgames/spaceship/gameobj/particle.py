import math
import random

import pygame


class Particle(pygame.sprite.Sprite):
    def __init__(self, pos, life):
        self.image = pygame.Surface([3, 3])
        self.rect = self.image.get_rect()
        self.rect = self.rect.move(pos)

        self.life = life
        self.maxlife = life

        self.v_pos = [float(self.rect.center[0]), float(self.rect.center[1])]

        self.direction = [random.randint(1.0, 50.0) * (random.randint(0, 1) * 2 - 1),
                          random.randint(1.0, 50.0) * (random.randint(0, 1) * 2 - 1)]
        self.magnitude = math.sqrt(self.direction[0] ** 2 + self.direction[1] ** 2)
        self.speed = random.randint(1, 100) / 33.333

        self.direction[0] = self.direction[0] / self.magnitude * self.speed
        self.direction[1] = self.direction[1] / self.magnitude * self.speed

    def update(self, screen):
        self.life -= 1
        self.dim = int(255 * (float(self.life) / self.maxlife))

        self.v_pos = [self.v_pos[0] + self.direction[0], self.v_pos[1] + self.direction[1]]

        self.rect = self.rect.move(int(self.v_pos[0]) - self.rect.center[0],
                                   int(self.v_pos[1]) - self.rect.center[1])

        self.color = random.randint(0, 3)
        if self.color == 0:
            self.image.fill([self.dim, self.dim, self.dim])
        elif self.color == 1:
            self.image.fill([self.dim, 0, 0])
        elif self.color == 2:
            self.image.fill([0, self.dim, 0])
        else:
            self.image.fill([0, 0, self.dim])

        screen.blit(self.image, self.rect)


class Explosion(pygame.sprite.Sprite):
    def __init__(self, pos):
        pygame.sprite.Sprite.__init__(self)

        self.life = 100

        self.particals = []
        for a in range(50):
            self.particals.append(Particle(pos, self.life))

    def update(self, screen):

        for partical in self.particals:
            partical.update(screen)

        self.life -= 1
