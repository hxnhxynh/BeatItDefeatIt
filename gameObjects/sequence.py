from pygame.locals import *
from . import Drawable
from random import randint
import pygame
import numpy as np


class Sequence(object):
   # array for all arrow info
   arrows = [[pygame.K_RIGHT,(0,0), (0,1), (0,2)],
             [pygame.K_UP,(1,0), (1,1), (1,2)],
             [pygame.K_LEFT,(2,0), (2,1), (2,2)],
             [pygame.K_DOWN,(3,0), (3,1), (3,2)]]

   
   def __init__(self, position, num):
      self.num = num
      self.sequence = []
      self.currentArrow = 0
      self.image = "arrowSheet.png"
      self.position = position
      self.complete = False
      self.size = position + (num*33, 0)

      # create n Drawable objects with random directions 
      for i in range(num):
         direction = randint(0,3)
         self.sequence.append((Drawable(position, \
                                       "arrowSheet.png",\
                                       self.arrows[direction][1]),
                              self.arrows[direction]))
         # add to the right 
         position += (33, 0)
         
      
   def handleEvent(self, event):
      if event.type == pygame.KEYDOWN:
         # if press correct direction
         if event.key == self.sequence[self.currentArrow][1][0]:
            arrow = self.sequence[self.currentArrow][0]
            direction = self.sequence[self.currentArrow][1]
            # change sprite to indicate it has been pressed
            arrow.changeImage("arrowSheet.png", direction[2])
            
            # move on to the next arrow!
            self.currentArrow += 1
            if self.currentArrow == self.num:
               self.complete = True
               self.currentArrow = self.num-1
   
   def update(self, seconds):
      pass

   def draw(self, drawSurface):
      for i in range(self.num):
         arrow = self.sequence[i][0]
         arrow.draw(drawSurface)
   
   
  
