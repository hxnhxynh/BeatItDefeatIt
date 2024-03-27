from FSMs import ScreenManagerFSM
from . import TextEntry, MouseMenu
from utils import vec, RESOLUTION, SoundManager
from gameObjects.engine import GameEngine, TutorialEngine, TutGameEngine
from pygame.locals import *

class ScreenManager(object):
    def __init__(self):
        self.game = GameEngine()
        self.tutorial = TutorialEngine()
        self.tutGame = TutGameEngine()
        self.state = ScreenManagerFSM(self)

        # startMenu portion
        self.startMenu = MouseMenu("background.png", hoverColor = (32, 214, 199))
        self.startMenu.addOption(key="start", 
                                 text="Game Mode", 
                                 position=(vec(RESOLUTION[0]//2, RESOLUTION[1]-70)),
                                 center="both", 
                                 unlocked=False)
        self.startMenu.addOption(key="tutorial", 
                                 text="Tutorial", 
                                 position=(vec(RESOLUTION[0]//2, RESOLUTION[1]-50)),
                                 center="both")
        self.startMenu.addImage((RESOLUTION//2 - vec(0,45)), "logo.png", center="both")


    def draw(self, drawSurface):
        if self.state.isInGame():
            self.game.draw(drawSurface)

        elif self.state.isInTutorial() :
            self.tutorial.draw(drawSurface)

        elif self.state.isInTutGame():
            self.tutGame.draw(drawSurface)
            
        elif self.state == "startMenu":
            self.startMenu.draw(drawSurface)
        

    def handleEvent(self, event):
        if self.state in ["game"]:
            if event.type == KEYDOWN and event.key == K_m:
                self.state.quitGame()
            else:
                self.game.handleEvent(event)

        elif self.state in ["tutorial"]:
            if event.type == KEYDOWN and event.key == K_m:
                self.state.quitTutorial()
            elif event.type == KEYDOWN and event.key == K_p:
                if self.tutorial.paused:
                    self.tutorial.paused = False
                else:
                    self.tutorial.paused = True
            elif self.tutorial.complete:
                self.state.startTutGame()
            else:
                if not self.tutorial.paused:
                    self.tutorial.handleEvent(event)
                    
        elif self.state in ["tutGame"]:
            if event.type == KEYDOWN and event.key == K_m:
                self.state.quitTutGame()
            elif event.type == KEYDOWN and event.key == K_p:
                if self.tutGame.paused:
                    self.tutGame.paused = False
                else:
                    self.tutGame.paused = True
            else:
                if not self.tutGame.paused:
                    self.tutGame.handleEvent(event)

        elif self.state == "startMenu":
            choice = self.startMenu.handleEvent(event)

            if choice == "tutorial":
                self.state.startTutorial()
    
    def update(self, seconds):
        if self.state == "game":
            self.game.update(seconds)
        elif self.state == "startMenu":
            self.startMenu.update(seconds)
        elif self.state == "tutorial":
            self.tutorial.update(seconds)
        elif self.state == "tutGame":
            self.tutGame.update(seconds)