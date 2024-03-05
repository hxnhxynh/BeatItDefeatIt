from gameObjects import Drawable 
import pygame
import os


class TextEntry(Drawable):
    if not pygame.font.get_init():
        pygame.font.init()

    FONT_FOLDER = "fonts"
    DEFAULT_FONT = "PressStart2P.ttf"
    DEFAULT_SIZE = 15

    FONTS = {"default" : pygame.font.Font(os.path.join(FONT_FOLDER, DEFAULT_FONT), DEFAULT_SIZE)
             }
    
    def __init__(self, position, text, font="default", color=(255,255,255)):
        super().__init__(position, "")
        self.position = position
        self.text = text
        self.font = font
        self.color = color
        self.image = TextEntry.FONTS[font].render(text, False, self.color)
        self.rect = self.image.get_rect()
        

    def changeColor(self, color=(0,0,0)):
        self.image = TextEntry.FONTS[self.font].render(self.text, False, color)

    def getRect(self):
        return self.rect


