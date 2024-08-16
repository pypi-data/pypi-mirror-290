from time import perf_counter as tpc
from typing import List

import pygame as pg

from base.bomb import Bomb
from base.button import Button
from base.constant import SCREEN_RECT, WINDOW_CAPTION
from base.player import Player
from base.spaceship import Alien
from base.utils import convert_color, load_image
from game.config import Config


class Game:
    def __init__(self, config: Config) -> None:
        self.is_running = True

        if pg.get_sdl_version()[0] == 2:
            pg.mixer.pre_init(44100, 32, 2, 1024)
        pg.init()
        if pg.mixer and not pg.mixer.get_init():
            print("Warning, no sound")
            pg.mixer = None

        self.config = config

        best_depth = pg.display.mode_ok(SCREEN_RECT.size, 0, 32)
        self.screen = pg.display.set_mode(self.config['window']['size'], 0, best_depth)
        pg.display.set_caption(self.config['window']['caption'])

        self.buttons: List[Button] = []
        x = self.screen.get_width() / 2 - self.config["ui"]["button"]["width"] / 2
        self.buttons.append(Button(self.screen, x, 200, "开始游戏"))

        Alien.images = [load_image(f"alien{x}.gif") for x in (1, 2, 3)]
        Bomb.images = [load_image("bomb.gif")]

        player_img = load_image("player1.gif")
        Player.images = [player_img, pg.transform.flip(player_img, 1, 0)]
        icon = pg.transform.scale(Alien.images[0], (32, 32))
        pg.display.set_icon(icon)

        self.bg = pg.Surface(SCREEN_RECT.size)
        self.screen.blit(self.bg, (0, 0))
        pg.display.flip()

        self.group_aliens = pg.sprite.Group()
        self.group_all = pg.sprite.RenderUpdates()

    def play(self):
        clock = pg.time.Clock()
        start_time = tpc()
        debug: bool = self.config["debug"]["open"]

        Alien(self.group_aliens, self.group_all)
        Player(self.group_all)

        while self.is_running:
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    return
                elif event.type == pg.KEYDOWN:
                    self.on_key_down(event)
                elif event.type == pg.MOUSEBUTTONDOWN:
                    mouse_x, mouse_y = pg.mouse.get_pos()
                    self.on_mouse_down(mouse_x, mouse_y)

            # self.on_render()
            self.on_logic()

            self.group_all.clear(self.screen, self.bg)
            self.group_all.update()

            # if debug:
            #    self.on_debug()

            dirty = self.group_all.draw(self.screen)
            pg.display.update(dirty)

            clock.tick(60)

    def on_render(self):
        self.screen.fill((0, 0, 0))

        for button in self.buttons:
            button.on_draw()

    def on_logic(self):
        pass

    def on_key_down(self, event: pg.event.Event):
        if event.key == pg.K_ESCAPE or event.key == pg.K_q:
            self.is_running = False

    def on_mouse_down(self, x: int, y: int):
        for button in self.buttons:
            if button.rect.collidepoint(x, y):
                button.on_click()

    def on_debug(self):
        grid_count = self.config["debug"]["grid_count"]
        grid_size = self.config["debug"]["grid_size"]
        grid_color = convert_color(self.config["debug"]["grid_color"])

        for x in range(1, grid_count):
            pg.draw.line(
                self.screen,
                grid_color,
                (x * grid_size, 0),
                (x * grid_size, self.screen.get_height()),
            )
