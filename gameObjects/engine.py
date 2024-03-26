import pygame
from . import Drawable, Sequence, TimingBar
from utils import vec, RESOLUTION, rectAdd, SCALE, SoundManager
from time import time

NUMARROWS = 5
SEQUENCE_SIZE = vec(32*NUMARROWS, 32)

class GameEngine(object):
    import pygame

    def __init__(self):       
        self.size = vec(*RESOLUTION)
        self.background = Drawable((0,0), "dasKlubBackground.png")
        self.sequence = Sequence(((RESOLUTION/2)-(SEQUENCE_SIZE[0]/2,-40)),
                                  NUMARROWS)
        self.timingBar = TimingBar(((RESOLUTION/2)-(SEQUENCE_SIZE[0]/2,0)))
        self.points = 0
        self.font1 =  pygame.font.SysFont("Harlow Solid", 15)
        self.font2 = pygame.font.SysFont("Arial", 15)
        self.pointDisplay = self.font1.render("Score count: 0",
                                             False,
                                             (255,255,255))
        self.instructions = self.font1.render("Press the arrow keys in order to earn points!",
                                             False,
                                             (255,255,255))
        self.scoreNotifs = {"bad" : self.font2.render("Bad! -100 points", 
                                                     False, 
                                                     (185, 191, 151)),
                            "good": self.font2.render("Good job! +300 points",
                                                     False,
                                                     (32, 214, 99)),
                            "great": self.font2.render("Great job! +500 points",
                                                      False,
                                                      (156, 219, 67)),
                            "perf": self.font2.render("Perfect! +1000 points", 
                                                     False,
                                                     (188, 74, 155))
                            }
    
    def draw(self, drawSurface):        
        self.background.draw(drawSurface)
        self.sequence.draw(drawSurface)
        self.timingBar.draw(drawSurface)
        drawSurface.blit(self.pointDisplay, (0,0))
        drawSurface.blit(self.instructions, (RESOLUTION[0]/2-(self.instructions.get_width()//2), RESOLUTION[1]-50))
        scoreNotif = self.scoreNotifs[self.timingBar.scoreType]
        if scoreNotif != None:
            drawSurface.blit(scoreNotif, (RESOLUTION[0]/2-(scoreNotif.get_width()//2), RESOLUTION[1]-70))

    def handleEvent(self, event):
        self.sequence.handleEvent(event)
        self.timingBar.handleEvent(event)
        if self.sequence.complete:
            if self.timingBar.complete: # if sequence is completed and space bar is hit
                self.timingBar.complete = False
                self.sequence = Sequence(((RESOLUTION/2)-(SEQUENCE_SIZE[0]/2,-40)),
                                      NUMARROWS) # reset sequence
                
                # increase and display points
                self.points += self.timingBar.score 
                self.pointDisplay = self.font1.render("Score count: " + str(self.points),
                                                     False,
                                                     (255,255,255))
        else:
            if self.timingBar.complete:
                self.timingBar.complete = False

                # penalty for pressing space bar w/o completing sequence
                self.points -= 100
                self.pointDisplay = self.font1.render("Score count: " + str(self.points),
                                                False,
                                                (255,255,255))
        
    
    def update(self, seconds):
        self.timingBar.update(seconds)
        #self.sequence.update(seconds)
        #Drawable.updateOffset(self.sequence, self.size)

class TutorialEngine(object):
    import pygame

    def __init__(self):   
        self.paused = False    
        self.size = vec(*RESOLUTION)
        self.background = Drawable((0,0), "dasKlubBackground.png")
        self.font1 =  pygame.font.SysFont("Harlow Solid", 15)
        self.font2 = pygame.font.SysFont("Arial Black", 15)

        self.box = Drawable((0,0), "instructions.png")
        self.start = False
        self.step1 = self.font2.render("1. Press the keys in order.", False, (255, 255, 255))
        self.step2 = self.font2.render("2. Press the space bar when reaching the middle of the CD.", False, (255, 255, 255))
        self.testSeq = Sequence(vec(50, 90), 5)
        self.testBar = TimingBar(vec(50, 197))
        self.ok = self.font2.render("Let's play!", False, (255, 255, 255))
        self.waiting = False
        self.wait = 4
        self.count = 0
        self.beatTimer = 0
        self.sequence = Sequence(((RESOLUTION/2)-(SEQUENCE_SIZE[0]/2,-40)),
                                  NUMARROWS)
        self.timingBar = TimingBar(((RESOLUTION/2)-(SEQUENCE_SIZE[0]/2,0)))
        self.points = 0
        self.pointDisplay = self.font1.render("Score count: 0",
                                             False,
                                             (255,255,255))
        #self.instructions = self.font1.render("Press the arrow keys in order to earn points!", False, (255,255,255))
        self.scoreNotifs = {"bad" : self.font2.render("Bad! +100 points", 
                                                     False, 
                                                     (245, 245, 245)),
                            "good": self.font2.render("Good job! +300 points",
                                                     False,
                                                     (0, 255, 255)),
                            "great": self.font2.render("Great job! +500 points",
                                                      False,
                                                      (0, 255, 0)),
                            "perf": self.font2.render("Perfect! +1000 points", 
                                                     False,
                                                     (255, 0, 255)),
                            "miss": self.font2.render("Miss! -100 points",
                                                      False,
                                                      (245, 245, 245))
                            }
    
    def draw(self, drawSurface):        
        self.background.draw(drawSurface)
        if self.start:
            self.timingBar.draw(drawSurface)
            if self.waiting:
                if time() - self.count >= self.wait:
                    self.waiting = False
                    self.timingBar.bar.play = True
                    
            else:
                self.sequence.draw(drawSurface)
                
            drawSurface.blit(self.pointDisplay, (0,0))
            scoreType =  self.timingBar.scoreType
            if scoreType != None:
                scoreNotif = self.scoreNotifs[scoreType]
                drawSurface.blit(scoreNotif, (RESOLUTION[0]/2-(scoreNotif.get_width()//2), RESOLUTION[1]-70))
        else:
            self.box.draw(drawSurface)

            drawSurface.blit(self.step1, (36, 67))
            drawSurface.blit(self.step2, (36, 167))

            self.testSeq.draw(drawSurface)
            self.testBar.draw(drawSurface)

            drawSurface.blit(self.ok, (480, 250))
            self.okHitBox = rectAdd((460, 250), self.ok.get_rect())
            

    def handleEvent(self, event):
        if self.start:
            self.sequence.handleEvent(event)
            self.timingBar.handleEvent(event)
            if self.sequence.complete:
                if self.timingBar.complete: # if sequence is completed and space bar is hit
                    self.timingBar.complete = False
                    self.sequence = Sequence(((RESOLUTION/2)-(SEQUENCE_SIZE[0]/2,-40)),
                                  NUMARROWS)
                    # increase and display points
                    self.points += self.timingBar.score 
                    self.pointDisplay = self.font1.render("Score count: " + str(self.points),
                                                        False,
                                                        (255,255,255)) 
                    self.counting = True         
            else:
                if self.timingBar.complete:
                    self.timingBar.complete = False

                    # penalty for pressing space bar w/o completing sequence
                    self.points -= 100
                    self.timingBar.scoreType = "miss"
                    self.pointDisplay = self.font1.render("Score count: " + str(self.points),
                                                    False,
                                                    (255,255,255))
        else:
            if self.okHitBox.collidepoint(vec(*pygame.mouse.get_pos())//SCALE):
                self.ok = self.font2.render("Let's play!", False, (0, 0, 0))
                if event.type == pygame.MOUSEBUTTONDOWN:
                    self.start = True
                    self.count = time()
                    self.waiting = True
            else:
                self.ok = self.font2.render("Let's play!", False, (255, 255, 255))
    
    def update(self, seconds):
        if self.start:
            if not self.paused:
                self.timingBar.update(seconds)
        else:
            self.testBar.update(seconds)
        #self.sequence.update(seconds)
        #Drawable.updateOffset(self.sequence, self.size)



