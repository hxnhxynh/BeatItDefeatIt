from . import AbstractGameFSM
from statemachine import State

class ScreenManagerFSM(AbstractGameFSM):
    startMenu = State(initial=True)
    game = State()
    paused = State()

    pause = game.to(paused) | paused.to(game) | startMenu.to.itself(internal=True)

    startGame = startMenu.to(game)
    quitGame = game.to(startMenu) | paused.to.itself(internal=True)

    def isInGame(self):
        return self == "game"