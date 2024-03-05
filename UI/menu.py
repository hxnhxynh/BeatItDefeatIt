from gameObjects import Drawable
from utils.vector import vec, magnitude, rectAdd
from utils.constants import SCALE
from . import TextEntry

import pygame

class AbstractMenu(Drawable):

    def __init__(self, background, fontName="default", color=(255,255,255)):
        super().__init__((0,0), background)
        self.options = {}
        self.color = color
        self.font = fontName

    def addOption(self, key, text, position, center=None):
        self.options[key] = TextEntry(position, text, self.font, self.color)
        optionSize = self.options[key].getSize()

        if center != None:
            if center == "both":
                offset = optionSize // 2
            elif center == "horizontal":
                offset = vec(optionSize[0] // 2, 0)
            elif center == "vertical":
                offset = vec(0, optionSize[1] // 2)
            else:
                offset = vec(0,0)
            
            self.options[key].position -= offset
            self.options[key].hitBox = rectAdd(self.options[key].position, self.options[key].rect)
    
    def draw(self, drawSurface):
        super().draw(drawSurface)

        for option in self.options.values():
            option.draw(drawSurface)

class EventMenu(AbstractMenu):
    
    def __init__(self, background, fontName="default", color=(255, 255, 255)):
        super().__init__(background, fontName, color)
        self.eventMap = {}
    
    def addOption(self, key, text, position, eventLamba, center=None):
        super().addOption(key, text, position, center)
        self.eventMap[key] = eventLamba

    def handleEvent(self, event):
        for key in self.eventMap.keys():
            function = self.eventMap[key]
            if function(event):
                return key

# uhhh freestyling a mouse/hover menu here...
class MouseMenu(AbstractMenu):
    def __init__(self, background, fontName="default", color=(255, 255, 255), hoverColor=(0,0,0)):
        super().__init__(background, fontName, color)
        self.hoverColor = hoverColor
        self.hovered = {}
    
    def addOption(self, key, text, position, center=None):
        super().addOption(key, text, position, center)
        self.hovered[key] = False

    def handleEvent(self, event):
        for key in self.options.keys():
            option = self.options[key]
            #print(option.hitBox)
            #print(option.position)
            if option.hitBox.collidepoint(vec(*pygame.mouse.get_pos())//SCALE):
                self.hovered[key] = True
                self.options[key].changeColor(self.hoverColor)
                if event.type == pygame.MOUSEBUTTONDOWN:
                    return key


            else:
                self.hovered[key] = False
                self.options[key].changeColor(self.color)
                    
