from pygame.locals import *
from . import Drawable, Animated, Interpolated
import pygame
import numpy as np
from utils import vec

class TimingBar(object):

    def __init__(self, position=vec(0,0), tempo=60):
        # basic info of timing bar
        self.position = position
        self.size = position + (160, 32)
        self.tempo = tempo
        self.complete = False

        # set up back
        self.back = Drawable(position, "timingBack.png")

        # set up cd
        self.cd = Animated(position+(112, 0), "cd.png")
        self.cd.nFrames = 4

        # set up hitbox boundaries
        self.stop = position + (154,0)
        self.bar = Interpolated(self.position, self.stop, 4, "timingBar.png")
        # need to move bar to 125 pixels to hit center of CD
        # every fourth beat of 60 bpm = 4 seconds , should move 38.5 pixels per second
        # 154 pixels = reset
        #self.bar.velocity= vec(38.5,0)
        self.score = 100 #default bad score
        self.scoreType = None
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

            