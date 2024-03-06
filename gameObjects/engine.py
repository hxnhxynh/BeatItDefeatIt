import pygame

from . import Drawable, Sequence, TimingBar

from utils import vec, RESOLUTION

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

