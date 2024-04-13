from utils import vec, Rect
from . import Drawable
import pygame

class Hitbox(Drawable):

    def __init__(self, position, width, height):
        super().__init__(position)
        self.image = (self.position[0], self.position[1], width, height)
        self.width = width
        self.height = height

    def draw(self, drawSurface):
        pygame.draw.rect(drawSurface, (255,0,0), self.image,2) 

    def getSize(self):
        return vec(self.width, self.height)
    
    def update(self, objectPos):
        self.image = (objectPos[0]- Drawable.CAMERA_OFFSET[0], objectPos[1]- Drawable.CAMERA_OFFSET[1], self.width, self.height)

    def getRect(self):
        return Rect(self.image)