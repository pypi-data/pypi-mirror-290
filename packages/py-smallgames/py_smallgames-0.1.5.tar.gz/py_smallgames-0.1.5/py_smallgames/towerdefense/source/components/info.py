import pygame
import yaml

from .. import constants as c

pygame.font.init()


class Info:
    def __init__(self, state):
        self.state = state
        self.state_labels = []
        self.create_state_labels()
        self.create_info_labels()

    def create_state_labels(self):
        with open(c.LABEL_CONFIG_PATH, 'r', encoding='utf-8') as f:
            config = yaml.load(f, Loader=yaml.FullLoader)

        if self.state == c.STATE_START:
            for label in config['main_menu']:
                self.state_labels.append((self.create_label(label['name']), label['pos']))

    def create_info_labels(self):
        pass

    def create_label(self, label: str, size=c.FONT_SIZE_DEFAULT, width_scale=1.25, height_scale=1):
        font = pygame.font.Font(c.FONT_IBMPLEX_PATH, size)
        label_image = font.render(label, True, (255, 255, 255))
        return label_image

    def update(self):
        pass

    def draw(self, screen: pygame.Surface):
        for label in self.state_labels:
            screen.blit(label[0], label[1])
