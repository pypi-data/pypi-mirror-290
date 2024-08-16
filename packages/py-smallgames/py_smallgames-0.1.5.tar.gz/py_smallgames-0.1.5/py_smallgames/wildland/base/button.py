import pygame
from base.constant import DIR_FONT
from base.sprite import Sprite


class Button(Sprite):
    FONT_SIZE = 25
    COLORS = ((128, 128, 128), (208, 132, 132))

    def __init__(self, screen: pygame.Surface, x: int, y: int, text: str) -> None:
        super().__init__()

        self.screen = screen
        self.rect = pygame.Rect(0, 0, 120, 30)
        self.rect.topleft = x, y
        self.text = text

        self.font = pygame.font.Font(DIR_FONT / "SourceHanSansCN-Bold.ttf")
        self.clicked = False

    def on_draw(self):
        color = self.COLORS[int(self.clicked)]
        self.screen.fill(color, self.rect)

        msg = self.font.render(self.text, True, (255, 0, 0))
        msg_rect = msg.get_rect()
        msg_rect.center = self.rect.center
        self.screen.blit(msg, msg_rect)

    def on_click(self):
        self.clicked = not self.clicked
