import random

import pygame

from py_smallgames.libs.gameobj.movingsprite import MovingSprite
from py_smallgames.spaceship.gameobj.shot import Shot


# class Enemy1(pygame.sprite.Sprite):
#     def __init__(self, pos):
#         pygame.sprite.Sprite.__init__(self)
#
#         self.image = pygame.image.load("assets/images/enemy1.gif")
#         self.rect = self.image.get_rect()
#
#         self.rect = self.rect.move(pos)
#
#         self.speed = random.randint(-2, -1)
#
#     def update(self, screen, time, ship):
#         self.rect = self.rect.move([self.speed, 0])
#         screen.blit(self.image, self.rect)


class Enemy1(MovingSprite):
    IMG = "assets/images/enemy1.gif"

    def __init__(
        self,
        pos,
    ):
        super().__init__(pos)
        self.image = pygame.Surface((30, 30))
        self.image.fill((255, 0, 0))
        self.vel = (random.randint(-2, -1), 0)


class Enemy2(pygame.sprite.Sprite):
    def __init__(self, pos, shot_list):
        pygame.sprite.Sprite.__init__(self)

        self.image = pygame.image.load("assets/images/enemy2.gif")
        self.rect = self.image.get_rect()

        self.rect = self.rect.move(pos)

        self.speed = random.randint(-2, -1)

        self.shot_list = shot_list

    def update(self, screen, time, ship):
        if ship != None:

            if abs(ship.rect.center[1] - self.rect.center[1]) < 10 and time % 20 == 0:
                self.shot_list.append(Shot(self.rect.center, "left"))

            if time % 2:
                if ship.rect.center[1] - self.rect.center[1] < 0:
                    self.rect = self.rect.move(0, -1 * -self.speed)
                if ship.rect.center[1] - self.rect.center[1] > 0:
                    self.rect = self.rect.move(0, 1 * -self.speed)

        self.rect = self.rect.move([self.speed, 0])
        screen.blit(self.image, self.rect)


class Enemy3(pygame.sprite.Sprite):
    def __init__(self, pos):
        pygame.sprite.Sprite.__init__(self)

        self.image = pygame.image.load("assets/images/enemy3.gif")

        ####
        self.image.set_colorkey([255, 255, 255])
        ####

        self.rect = self.image.get_rect()

        self.rect = self.rect.move(pos)

        self.speed = -6

    def update(self, screen, time, ship):
        if ship != None:
            if time % 2:
                if ship.rect.center[1] - self.rect.center[1] < 0:
                    self.rect = self.rect.move(0, -1 * -self.speed)
                if ship.rect.center[1] - self.rect.center[1] > 0:
                    self.rect = self.rect.move(0, 1 * -self.speed)

        self.rect = self.rect.move([self.speed, 0])
        screen.blit(self.image, self.rect)
