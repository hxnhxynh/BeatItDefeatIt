import pygame

from . import Drawable, Sequence

from utils import vec, RESOLUTION

NUMARROWS = 5
SEQUENCE_SIZE = vec(32*NUMARROWS, 32)

class GameEngine(object):
    import pygame

    def __init__(self):       
        self.size = vec(*RESOLUTION)
        self.background = Drawable((0,0), "dasKlubBackground.png")
        self.sequence = Sequence(((RESOLUTION/2)-(SEQUENCE_SIZE[0]/2,-16)),
                                  NUMARROWS)
        self.points = 0
        self.font =  pygame.font.SysFont("Harlow Solid", 15)
        self.pointDisplay = self.font.render("Score count: 0",
                                             False,
                                             (255,255,255))
        self.instructions = self.font.render("Press the arrow keys in order to earn points!",
                                             False,
                                             (255,255,255))

    
    def draw(self, drawSurface):        
        self.background.draw(drawSurface)
        self.sequence.draw(drawSurface)
        drawSurface.blit(self.pointDisplay, (0,0))
        drawSurface.blit(self.instructions, (RESOLUTION[0]/2-(self.instructions.get_width()//2), RESOLUTION[1]-50))

    def handleEvent(self, event):
        self.sequence.handleEvent(event)
        if self.sequence.complete:
            self.sequence = Sequence(((RESOLUTION/2)-(SEQUENCE_SIZE[0]/2,-16)),
                                  NUMARROWS)
            self.points += 100
            self.pointDisplay = self.font.render("Score count: " + str(self.points),
                                             False,
                                             (255,255,255))
        
    
    def update(self, seconds):
        pass
        #self.sequence.update(seconds)
        #Drawable.updateOffset(self.sequence, self.size)
    

