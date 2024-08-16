import source.constants as c
from source.game import Game
from source.states import start, level, end


def main():
    state_dict = {
        c.STATE_START: start.StartState(),
        c.STATE_LEVEL: level.LevelState(),

        # TODO: ranking level
        c.STATE_END: end.EndState()
    }

    game = Game(state_dict, c.STATE_START)
    game.run()


if __name__ == '__main__':
    main()
