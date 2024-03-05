from FSMs import ScreenManagerFSM
from . import TextEntry, MouseMenu
from utils import vec, RESOLUTION
from gameObjects.engine import GameEngine
from pygame.locals import *

class ScreenManager(object):
    def __init__(self):
        self.game = GameEngine()
        self.state = ScreenManagerFSM(self)

        # startMenu portion
        self.startMenu = MouseMenu("background.png")
        self.startMenu.addOption(key="start", 
                                 text="Tutorial", 
                                 position=(RESOLUTION//2 - vec(0,50)),
                                 center="both")


    def draw(self, drawSurface):
        if self.state.isInGame():
            self.game.draw(drawSurface)
            
        elif self.state == "startMenu":
            self.startMenu.draw(drawSurface)

    def handleEvent(self, event):
        if self.state in ["game"]:
            if event.type == KEYDOWN and event.key == K_m:
                self.state.quitGame()
            else:
                self.game.handleEvent(event)
        elif self.state == "startMenu":
            choice = self.startMenu.handleEvent(event)

            if choice == "start":
                self.state.startGame()
    
    def update(self, seconds):
        if self.state == "game":
            self.game.update(seconds)
        elif self.state == "startMenu":
            self.startMenu.update(seconds)