import os

import pygame

from .. import constants as c
from .. import setup


class Map(pygame.sprite.Sprite):
    """背景精灵"""

    def __init__(self, map_id: int):
        super().__init__()

        self.path_list = []
        self.map_elements = {
            0: setup.GRAPHICS['grass'],
            1: setup.GRAPHICS['rock'],
            2: setup.GRAPHICS['dirt'],
            3: setup.GRAPHICS['water'],
            4: setup.GRAPHICS['bush'],
            5: setup.GRAPHICS['nexus'],
            6: setup.GRAPHICS['cave'],
        }

        self.image = pygame.Surface(c.MAP_SIZE)
        map_file_path = os.path.join(c.MAP_DIR, f'{map_id}.map')
        self.load(map_file_path)
        self.rect = self.image.get_rect()
        self.rect.center = c.MAP_W / 2, c.MAP_H / 2

    def update(self):
        pass

    def load(self, file_path: str):
        row_index = -1
        with open(file_path, 'r') as map_file:
            for line in map_file.readlines():
                line = line.strip()
                if not line:
                    continue

                row_index += 1
                col_index = -1
                for col in line:
                    element_id = int(col)
                    element_img = self.map_elements.get(element_id)
                    element_rect = element_img.get_rect()

                    col_index += 1
                    element_rect.left = c.TILE_SIZE * col_index
                    element_rect.top = c.TILE_SIZE * row_index
                    self.image.blit(element_img, element_rect)

                    if element_id == 1:
                        self.path_list.append((col_index, row_index))
