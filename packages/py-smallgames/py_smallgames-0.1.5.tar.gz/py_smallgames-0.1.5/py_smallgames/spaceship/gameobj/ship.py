import pygame


class Ship(pygame.sprite.Sprite):
    def __init__(self, size):
        pygame.sprite.Sprite.__init__(self)

        self.image = pygame.image.load("assets/images/ship.gif")
        self.rect = self.image.get_rect()

        self.rect = self.rect.move(size[0] / 8, size[1] / 2)

        self.speed = 4

    def update(self, screen, keys, size):

        # move
        if keys[pygame.K_UP]:
            self.rect = self.rect.move(0, -self.speed)
        if keys[pygame.K_DOWN]:
            self.rect = self.rect.move(0, self.speed)
        if keys[pygame.K_LEFT]:
            self.rect = self.rect.move(-self.speed, 0)
        if keys[pygame.K_RIGHT]:
            self.rect = self.rect.move(self.speed, 0)

        # bounce
        if self.rect.top < 0:
            self.rect = self.rect.move(0, self.speed)
        if self.rect.bottom > size[1]:
            self.rect = self.rect.move(0, -self.speed)
        if self.rect.left < 0:
            self.rect = self.rect.move(self.speed, 0)
        if self.rect.right > size[0]:
            self.rect = self.rect.move(-self.speed, 0)

        # render
        screen.blit(self.image, self.rect)
