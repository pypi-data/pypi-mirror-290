import pygame
from pygame.locals import *
from sys import exit
from random import randint
from GameMap import *
from AStarSearch import *
from RogueLikeMaze import *
from GameRole import *
from enum import Enum

FRAME_RATE = 60
HERO_SPEED = 1


class BUTTON_TYPE(Enum):
    BUTTON_PLAY = (0,)
    BUTTON_FROG = (1,)
    BUTTON_REST = (2,)


button_types = {
    BUTTON_TYPE.BUTTON_PLAY: "Play",
    BUTTON_TYPE.BUTTON_FROG: "Frog",
    BUTTON_TYPE.BUTTON_REST: "Reset",
}


class Button:
    def __init__(self, screen, type, x, y):
        self.screen = screen
        self.width = BUTTON_WIDTH
        self.height = BUTTON_HEIGHT
        self.button_color = (128, 128, 128)
        self.text_color = [(0, 255, 0), (255, 0, 0)]
        self.font = pygame.font.SysFont(None, BUTTON_HEIGHT * 2 // 3)

        self.rect = pygame.Rect(0, 0, self.width, self.height)
        self.rect.topleft = (x, y)
        self.type = type
        self.click = False
        self.init_msg()

    def init_msg(self):
        self.msg_image = self.font.render(
            button_types[self.type], True, self.text_color[0], self.button_color
        )
        self.msg_image_rect = self.msg_image.get_rect()
        self.msg_image_rect.center = self.rect.center

    def draw(self):
        self.screen.fill(self.button_color, self.rect)
        self.screen.blit(self.msg_image, self.msg_image_rect)

    def on_click(self, game):
        self.click = not self.click
        if self.type == BUTTON_TYPE.BUTTON_PLAY:
            pass
        elif self.type == BUTTON_TYPE.BUTTON_FROG:
            game.hasFrog = self.click
        if self.click:
            index = 1
        else:
            index = 0
        self.msg_image = self.font.render(
            button_types[self.type], True, self.text_color[index], self.button_color
        )


class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode(
            [SCREEN_WIDTH + INFO_SHOW_WIDTH, SCREEN_HEIGHT + BUTTON_HEIGHT]
        )
        self.clock = pygame.time.Clock()
        self.map = Map(REC_X_NUM, REC_Y_NUM)
        self.screen_show = ScreenShow(
            SCREEN_WIDTH, SCREEN_HEIGHT, INFO_SHOW_WIDTH, BUTTON_HEIGHT, self.map
        )
        self.enemy_groups = []
        self.mode = 0
        self.buttons = []
        self.buttons.append(
            Button(self.screen, BUTTON_TYPE.BUTTON_PLAY, INFO_SHOW_WIDTH, 0)
        )
        self.buttons.append(
            Button(
                self.screen,
                BUTTON_TYPE.BUTTON_FROG,
                INFO_SHOW_WIDTH + BUTTON_WIDTH + 10,
                0,
            )
        )
        self.buttons.append(
            Button(
                self.screen,
                BUTTON_TYPE.BUTTON_REST,
                INFO_SHOW_WIDTH + (BUTTON_WIDTH + 10) * 2,
                0,
            )
        )
        self.hero = None
        self.hasFrog = False

    def play(self):
        def checkBulletCollide(enemy_groups, bullets_group):
            for group in self.enemy_groups:
                for bullet_group in bullets_group:
                    group.checkBulletCollide(bullet_group)

        def checkHeroCollide(enemy_groups, hero):
            for group in self.enemy_groups:
                group.checkHeroCollide(hero)

        time_passed = self.clock.tick(FRAME_RATE)

        pygame.draw.rect(
            self.screen, (255, 255, 255), pygame.Rect(0, 0, SCREEN_WIDTH, BUTTON_HEIGHT)
        )
        for button in self.buttons:
            button.draw()

        if self.hero is not None:
            self.hero.play(self.screen_show, action, time_passed)
            checkBulletCollide(self.enemy_groups, self.hero.weapon_groups)
            checkHeroCollide(self.enemy_groups, self.hero)

        self.screen_show.drawBackground(self.screen)

        if self.hero is not None:
            for weapon_group in self.hero.weapon_groups:
                weapon_group.update()
                weapon_group.draw(self.screen)
            self.hero.draw(self.screen_show)
            self.screen_show.showHeroInfo(self.screen, self.hero)

        for group in self.enemy_groups:
            group.process(time_passed, self.screen_show)
            group.render(self.screen, self.screen_show)

    def isOver(self):
        if self.hero is not None:
            return self.hero.isDead()
        return False

    def resetGame(self):
        self.map.resetMap(MAP_ENTRY_TYPE.MAP_EMPTY)
        self.map.resetFrog(0)
        self.hero = None
        self.enemy_groups = []

    def generateMaze(self):
        if self.mode >= 9:
            self.mode = 0
        if self.mode == 0:
            self.map.resetMap(MAP_ENTRY_TYPE.MAP_BLOCK)
            room_max_size = (
                self.map.width // 10
                if self.map.width < self.map.height
                else self.map.height // 10
            )
            ROOM_NUM = max(50, room_max_size * 20)
            addRooms(self.map, ROOM_NUM, room_max_size)
            print(MOVE_DIRECTION.MOVE_RIGHT.value)
        elif self.mode == 1:
            growMaze(self.map, (self.map.width - 1) // 2, (self.map.height - 1) // 2)

        elif self.mode == 2:
            connectRegions(
                self.map, (self.map.width - 1) // 2, (self.map.height - 1) // 2
            )
        elif self.mode == 3:
            # addReduentConnect(self.map, (self.map.width-1)//2, (self.map.height-1)//2, 8)
            connectReduentRooms(self.map, self.map.width, self.map.height, 3)
        elif self.mode == 4:
            removeDeadEnds(
                self.map, (self.map.width - 1) // 2, (self.map.height - 1) // 2
            )
        elif self.mode == 5:
            if self.hasFrog:
                self.map.resetFrog(1)
        elif self.mode == 6:
            self.source = self.map.generateEntityPos(
                (1, self.map.width // 5), (1, self.map.height // 5)
            )
            screen_x, screen_y = self.screen_show.mapIndexToScreen(
                self.source[0], self.source[1]
            )
            hero_surface = initHeroSurface()
            weapon_groups = initWeaponGroups()
            self.hero = Hero(
                self.screen,
                self.source[0],
                self.source[1],
                screen_x,
                screen_y,
                weapon_groups,
                hero_surface,
            )
            self.hero.update(self.screen_show)
            print("hero(%d,%d)" % (self.source[0], self.source[1]))
            self.dest = self.map.generateEntityPos(
                (self.map.width * 4 // 5, self.map.width - 2), (1, self.map.height - 2)
            )
            self.map.clearFrog(self.source[0], self.source[1], 5)
            self.map.clearFrog(self.dest[0], self.dest[1], 0)
            # self.map.setMap(self.source[0], self.source[1], MAP_ENTRY_TYPE.MAP_TARGET)

            self.map.setMap(self.dest[0], self.dest[1], MAP_ENTRY_TYPE.MAP_TARGET)
        elif self.mode == 7:
            createEnemy(self.screen_show, self.map, self.enemy_groups, self.hero)
        # 	AStarSearch(self.map, self.source, self.dest)
        # 	self.map.setMap(self.source[0], self.source[1], MAP_ENTRY_TYPE.MAP_TARGET)
        # 	self.map.setMap(self.dest[0], self.dest[1], MAP_ENTRY_TYPE.MAP_TARGET)
        else:
            self.resetGame()
        self.mode += 1


def check_buttons(game_, mouse_x, mouse_y):
    for button in game_.buttons:
        if button.rect.collidepoint(mouse_x, mouse_y):
            button.on_click(game_)
            break


def main():
    offset = {
        pygame.K_LEFT: (-1, 0, MOVE_DIRECTION.MOVE_LEFT),
        pygame.K_RIGHT: (1, 0, MOVE_DIRECTION.MOVE_RIGHT),
        pygame.K_UP: (0, -1, MOVE_DIRECTION.MOVE_UP),
        pygame.K_DOWN: (0, 1, MOVE_DIRECTION.MOVE_DOWN),
    }

    game = Game()
    action = None

    while True:
        if game.isOver():
            print("Game over")
            game.resetGame()
        else:
            game.play()
        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.KEYDOWN:
                if event.key in offset:
                    action = offset[event.key]
                elif event.key == pygame.K_SPACE:
                    game.generateMaze()
                    break
                elif event.key == pygame.K_x:
                    if game.hero is not None:
                        game.hero.setShoot()
            elif event.type == pygame.KEYUP:
                if event.key in offset:
                    action = None
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_x, mouse_y = pygame.mouse.get_pos()
                check_buttons(game, mouse_x, mouse_y)


if __name__ == "__main__":
    main()
