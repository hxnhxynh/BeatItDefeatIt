from . import AbstractGameFSM
from statemachine import State

class ScreenManagerFSM(AbstractGameFSM):
    startMenu = State(initial=True)
    game = State()
    intro = State()
    paused = State()
    tutorial = State()
    tutGame = State()

    pause = game.to(paused) | paused.to(game) | startMenu.to.itself(internal=True) | tutorial.to(paused) | paused.to(tutorial) | tutGame.to(paused) | paused.to(tutGame)\
        |intro.to(paused) | paused.to(intro)

    startIntro = startMenu.to(intro)
    quitIntro = intro.to(startMenu) | paused.to.itself(internal=True)

    startGame = intro.to(game)
    quitGame = game.to(startMenu) | paused.to.itself(internal=True)

    startTutorial = startMenu.to(tutorial)
    quitTutorial = tutorial.to(startMenu) | paused.to.itself(internal=True)

    startTutGame = tutorial.to(tutGame)
    quitTutGame = tutGame.to(startMenu) | paused.to.itself(internal=True)

    def isInGame(self):
        return self == "game"
    
    def isInTutorial(self):
        return self == "tutorial"
    
    def isInTutGame(self):
        return self == "tutGame"
    
    def isInIntro(self):
        return self == "intro"