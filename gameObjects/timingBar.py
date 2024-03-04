from pygame.locals import *
from . import Drawable, Animated, Mobile
import pygame
import numpy as np
from utils import vec

class TimingBar(object):

    def __init__(self, position=vec(0,0)):
        # basic info of timing bar
        self.position = position
        self.size = position + (160, 32)
        self.complete = False

        # set up back
        self.back = Drawable(position, "timingBack.png")

        # set up cd
        self.cd = Animated(position+(128, 0), "cd.png")
        self.cd.nFrames = 4

        # set up hitbox boundaries
        self.bar = Mobile(position, "timingBar.png")
        self.bar.velocity= vec(40,0)
        self.score = 100 #default bad score
        self.scoreType = "bad"
        self.goodOffSet = 6
        self.greatOffSet = 11
        self.perfOffset = 15

    def draw(self, drawSurface):
        self.back.draw(drawSurface)
        self.cd.draw(drawSurface)
        self.bar.draw(drawSurface)

    def update(self, seconds):
        self.cd.update(seconds)
        self.bar.update(seconds)
        if self.bar.position[0] - self.size[0] > 0:
            self.bar = Mobile(self.position, "timingBar.png")
            self.bar.velocity= vec(40,0)

    def handleEvent(self, event):
        if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
            self.complete = True
            current = self.bar.position[0]
            cdStart = self.cd.position[0]
            cdMid = cdStart + 16
            if current >= cdStart:
                if current <= self.goodOffSet + cdStart :
                    #print("good, + 300 to", self.score)
                    self.score = 300
                    self.scoreType = "good"
                elif current <= self.greatOffSet + cdStart:
                    #print("great, + 500 to", self.score)
                    self.score = 500
                    self.scoreType = "great"
                elif current <= self.perfOffset + cdStart:
                    #print("perf, + 1000 to", self.score)
                    self.score = 1000
                    self.scoreType = "perf"
            elif current >= cdMid:
                if current <= self.greatOffSet-1 + cdMid:
                    #print("great, + 500 to", self.score)
                    self.score = 500
                    self.scoreType = "great"
                elif current <= self.goodOffSet + cdMid:
                    #print("good, + 300 to", self.score)
                    self.score = 300
                    self.scoreType = "good"
            else:
                #print("bad, + 100 to", self.score)
                self.score = 100
                self.scoreType = "bad"

            