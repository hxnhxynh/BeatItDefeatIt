from . import Mobile
from FSMs import WalkingFSM, AccelerationFSM
from utils import rectAdd
from pygame.locals import *
import pygame
import numpy as np

class Player(Mobile):
    
    def __init__(self, position):
        super().__init__(position, "playerSheet.png")

        self.framesPerSecond = 2
        self.nFrames = 8

        self.nFramesList = {
            "standing" : 4,
            "moving" : 8
        }

        self.rowList = {
            "standing" : 0,
            "moving": 1
        }

        self.framesPerSecondList = {
            "standing": 4,
            "moving": 8 
        }

        self.FSManimated = WalkingFSM(self)
        self.LR = AccelerationFSM(self, axis=0)
        self.hitbox = (self.position[0], self.position[1], 47, 47)

    def handleEvent(self, event):
      if event.type == KEYDOWN:
            
         if event.key == K_LEFT:
            self.LR.decrease()
            
         elif event.key == K_RIGHT:
            self.LR.increase()
            
      elif event.type == KEYUP:
             
            
         if event.key == K_LEFT:
            self.LR.stop_decrease()
            
         elif event.key == K_RIGHT:
            self.LR.stop_increase()
    
    def update(self, seconds): 
      self.LR.updateState()
      self.LR.update(seconds)
      super().update(seconds)