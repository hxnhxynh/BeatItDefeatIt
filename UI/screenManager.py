from FSMs import ScreenManagerFSM, MovementFSM
from . import TextEntry, MouseMenu
from utils import vec, RESOLUTION, SoundManager
from gameObjects.engine import LizLoungeEngine, LizStageEngine, LizBattle, TutorialEngine, TutGameEngine, IntroEngine
from gameObjects.drawable import Drawable
from pygame.locals import *
import pygame

class ScreenManager(object):
    import pygame
    def __init__(self):
        self.game = LizLoungeEngine()
        self.lizLounge = self.game
        self.lizStage = LizStageEngine()
        self.intro = IntroEngine()
        self.tutorial = TutorialEngine()
        self.tutGame = TutGameEngine()
        self.state = ScreenManagerFSM(self)
        self.lizBattle = LizBattle()

        # transitions in between game locations
        self.fading = False
        self.fade =  pygame.Surface(list(map(int, RESOLUTION))) 
        self.alpha = 255
        self.fade.set_alpha(255)                
        self.fade.fill((0,0,0))

        # startMenu portion
        self.startMenu = MouseMenu("background.png", hoverColor = (32, 214, 199))
        self.startMenu.addOption(key="intro", 
                                 text="Game Mode", 
                                 position=(vec(RESOLUTION[0]//2, RESOLUTION[1]-70)),
                                 center="both", 
                                 unlocked=True)
        self.startMenu.addOption(key="tutorial", 
                                 text="Tutorial", 
                                 position=(vec(RESOLUTION[0]//2, RESOLUTION[1]-50)),
                                 center="both")
        self.startMenu.addOption(key="test",
                                 text="Test", 
                                 position=(vec(RESOLUTION[0]//2, RESOLUTION[1]-30)),
                                 center="both")
        self.startMenu.addImage((RESOLUTION//2 - vec(0,45)), "logo.png", center="both")


    def draw(self, drawSurface):
        if self.state.isInGame():
            if self.game.transition:
                self.fading = True
            else: 
                self.game.draw(drawSurface)
                if self.fading:
                    drawSurface.blit(self.fade, (0,0))

        elif self.state.isInTutorial() :
            self.tutorial.draw(drawSurface)

        elif self.state.isInTutGame():
            self.tutGame.draw(drawSurface)
        
        elif self.state.isInIntro():
            self.intro.draw(drawSurface)
            
        elif self.state == "startMenu":
            self.startMenu.draw(drawSurface)
        

    def handleEvent(self, event):
        if self.state in ["game"]:
            if event.type == KEYDOWN and event.key == K_m:
                self.state.quitGame()
                Drawable.CAMERA_OFFSET = vec(0,0)

            elif self.game.transition:
                if self.game.area == "lizLounge":
                    if self.game.goTo == "lizStage":
                        self.game.goTo = None
                        self.game.transition = False
                        self.game = self.lizStage
                        Drawable.CAMERA_OFFSET = vec(0,0)
                        MovementFSM.WORLD_SIZE = vec(600,300)
                        self.fading = True
                        
                if self.game.area == "lizStage":
                    if self.game.goTo == "lizLounge":
                        self.game.goTo = None
                        self.game.transition = False
                        self.game = self.lizLounge
                        MovementFSM.WORLD_SIZE = vec(1000,300)
                        self.fading = True

                    elif self.game.readyToBattle:
                        self.game.readyToBattle = False
                        self.game.transition = False
                        self.game = self.lizBattle
                        Drawable.CAMERA_OFFSET = vec(0,0)
                        MovementFSM.WORLD_SIZE = vec(600,300)
                        self.fading = True
                        
            
            self.game.handleEvent(event)

        elif self.state in ["intro"]:
            if event.type == KEYDOWN and event.key == K_m:
                self.state.quitIntro()
            elif self.intro.back:
                self.state.quitIntro()
            elif self.intro.complete:
                self.state.startGame()
            else:
                self.intro.handleEvent(event)

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
                sm = SoundManager.getInstance()
                sm.playBGM("Disco  Drum Metronome Loop  60 BPM.mp3")
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

            if choice == "intro":
                self.state.startIntro()

            if choice == "test":
                self.game = self.lizBattle
                self.state.startGame()
    
    def update(self, seconds):
        if self.state == "game":
            self.game.update(seconds)
            if self.fading:
                self.alpha -= 2
                if self.alpha < 0:
                    self.fading = False
                    self.alpha = 255
                self.fade.set_alpha(self.alpha)
        elif self.state == "intro":
            self.intro.update(seconds)
        elif self.state == "startMenu":
            self.startMenu.update(seconds)
        elif self.state == "tutorial":
            self.tutorial.update(seconds)
        elif self.state == "tutGame":
            self.tutGame.update(seconds)