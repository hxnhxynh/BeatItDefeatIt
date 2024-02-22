import pygame

from . import Drawable, Sequence

from utils import vec, RESOLUTION

NUMARROWS = 5
SEQUENCE_SIZE = vec(32*NUMARROWS, 32)

class GameEngine(object):
    import pygame

    def __init__(self):       
        self.size = vec(*RESOLUTION)
        self.background = Drawable((0,0), "background.png")
        self.sequence = Sequence(((RESOLUTION/2)-(SEQUENCE_SIZE[0]/2,16)),
                                  NUMARROWS)
        self.points = 0
        self.font =  pygame.font.SysFont("Arial", 25)
        self.pointDisplay = self.font.render("Score count: 0",
                                             False,
                                             (255,255,255))

    
    def draw(self, drawSurface):        
        self.background.draw(drawSurface)
        self.sequence.draw(drawSurface)
        drawSurface.blit(self.pointDisplay, (0,0))
            
    def handleEvent(self, event):
        self.sequence.handleEvent(event)
        if self.sequence.complete:
            self.sequence = Sequence(((RESOLUTION/2)-(SEQUENCE_SIZE[0]/2,16)),
                                  NUMARROWS)
            self.points += 100
            self.pointDisplay = self.font.render("Score count: " + str(self.points),
                                             False,
                                             (255,255,255))
        
    
    def update(self, seconds):
        pass
        #self.sequence.update(seconds)
        #Drawable.updateOffset(self.sequence, self.size)
    

