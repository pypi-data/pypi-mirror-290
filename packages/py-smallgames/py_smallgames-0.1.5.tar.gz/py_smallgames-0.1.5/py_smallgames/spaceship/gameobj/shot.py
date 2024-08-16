import pygame


class Shot(pygame.sprite.Sprite):
    def __init__(self, pos, direction):
        pygame.sprite.Sprite.__init__(self)

        self.image = pygame.Surface([6, 6])
        pygame.draw.circle(self.image, [255, 255, 255], [3, 3], 3)
        self.image.set_colorkey([0, 0, 0])

        self.rect = self.image.get_rect()
        self.rect = self.rect.move(pos)

        self.direction = direction

    def update(self, screen):
        if self.direction == 'right':
            self.rect = self.rect.move(5, 0)
        else:
            self.rect = self.rect.move(-5, 0)
        screen.blit(self.image, self.rect)
