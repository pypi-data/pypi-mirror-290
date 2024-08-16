from pathlib import Path
import pygame as pg

DIR_SRC = Path(__file__).parent.parent
DIR_ASSETS = DIR_SRC / "assets"
DIR_FONT = DIR_ASSETS / "fonts"

assert all([x.is_dir() for x in (DIR_SRC, DIR_ASSETS, DIR_FONT)])


SCREEN_RECT = pg.Rect(0, 0, 640, 480)
FULL_SCREEN = False
WINDOW_CAPTION = "蛮荒大陆"
