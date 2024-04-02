from utils.vector import vec
from . import Drawable 
import pygame
import os


class Dialogue(Drawable):
    if not pygame.font.get_init():
        pygame.font.init()

    FONT_FOLDER = "fonts"
    DEFAULT_FONT = "PressStart2P.ttf"
    DEFAULT_SIZE = 15

    FONTS = {"default" : pygame.font.Font(os.path.join(FONT_FOLDER, DEFAULT_FONT), DEFAULT_SIZE)
             }
    
    def __init__(self, text, font="default", color=(255,255,255), begin="NPC", end="Player"):
        self.position = vec(40, 210)
        self.text = text
        self.sentences = self.text.split('\n') 
        self.font = font
        self.color = color
        if begin != "NPC": 
            self.box = Drawable((0,0), "dialogueBox.png", (0,0))
        else:
            self.box = Drawable((0,0), "dialogueBox.png", (1,0))
        self.limit = (560,270)
        self.next = None
        

        if len(self.sentences) == 1:
            super().__init__((40, 210), "")
            self.image = Dialogue.FONTS[font].render(text, False, self.color)
        else:
            self.images = self.makeText(self.sentences)                                                                                                                                                                                                                                                                                                                                                                                                                           
        

    def changeColor(self, color=(0,0,0)):
        self.image = Dialogue.FONTS[self.font].render(self.text, False, color)
    
    def draw(self, drawSurface):
        self.box.draw(drawSurface)
        if len(self.sentences) == 1:
            super().draw(drawSurface)
        else:
            for sentence in self.images:
                sentence.draw(drawSurface)

    def makeText(self, sentences):
        position = self.position
        rendered = []
        for i in range(len(sentences)):
            text = Drawable(position, "")
            text.image = Dialogue.FONTS[self.font].render(sentences[i], False, self.color)
            rendered.append(text)
            position = position + vec(0, 16)
        
        return rendered
    
    def add(self, text, begin="NPC", end="Player"):
        self.next = Dialogue(text, font = self.font, color = self.color)
    
    def handleEvent(self, event):
        if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
            return True



