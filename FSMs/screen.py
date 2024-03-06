from . import AbstractGameFSM
from statemachine import State

class ScreenManagerFSM(AbstractGameFSM):
    startMenu = State(initial=True)
    game = State()
    paused = State()
    tutorial = State()

    pause = game.to(paused) | paused.to(game) | startMenu.to.itself(internal=True) | tutorial.to(paused) | paused.to(tutorial)

    startGame = startMenu.to(game)
    quitGame = game.to(startMenu) | paused.to.itself(internal=True)

    startTutorial = startMenu.to(tutorial)
    quitTutorial = tutorial.to(startMenu) | paused.to.itself(internal=True)

    def isInGame(self):
        return self == "game"
    
    def isInTutorial(self):
        return self == "tutorial"