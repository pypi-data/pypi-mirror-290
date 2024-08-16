import os

WINDOW_W, WINDOW_H = 800, 600
WINDOW_SIZE = (WINDOW_W, WINDOW_H)
MAP_W, MAP_H = WINDOW_W, 500
MAP_SIZE = (MAP_W, MAP_H)
TILE_SIZE = 20

GAME_FPS = 120

BASE_DIR = os.path.abspath(os.curdir)
SOURCE_DIR = os.path.join(BASE_DIR, 'source')
DATA_DIR = os.path.join(SOURCE_DIR, 'data')
RESOURCE_DIR = os.path.join(BASE_DIR, 'resources')
FONT_DIR = os.path.join(RESOURCE_DIR, 'fonts')
GRAPHICS_DIR = os.path.join(RESOURCE_DIR, 'graphics')
MAP_DIR = os.path.join(RESOURCE_DIR, 'maps')
MUSIC_DIR = os.path.join(RESOURCE_DIR, 'music')
SOUND_DIR = os.path.join(RESOURCE_DIR, 'sound')

LABEL_CONFIG_PATH = os.path.join(DATA_DIR, 'labels.yaml')
assert os.path.isfile(LABEL_CONFIG_PATH)

FONT_IBMPLEX_PATH = os.path.join(FONT_DIR, 'IBMPlexSans-Regular.ttf')
FONT_SIZE_DEFAULT = 40
assert os.path.isfile(FONT_IBMPLEX_PATH)

STATE_START = 1
STATE_LEVEL = 2
STATE_END = 3

CURSOR_POS_X0, CURSOR_POS_Y0 = 140, 152
CURSOR_POS_Y1 = 202
