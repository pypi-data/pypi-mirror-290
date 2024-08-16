import pygame as pg

from base.constant import DIR_ASSETS
from game.config import Config
from game.game import Game


def main():
    config = Config(str(DIR_ASSETS / "config.toml"))
    game = Game(config=config)
    game.play()
    pg.quit()


if __name__ == "__main__":
    main()
