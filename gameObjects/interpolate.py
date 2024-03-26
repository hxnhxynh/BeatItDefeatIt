from utils.vector import vec
from . import Drawable

class Interpolated(Drawable):
    def __init__(self, start, stop, seconds, fileName=""):
        super().__init__(start, fileName, (0,0))
        self.fileName = fileName
        self.start = start[0]
        self.stop = stop[0]
        self.seconds = seconds
        self.step = (self.stop-self.start)/self.seconds
        self.timer = 0
        self.loop = True

    def update(self, seconds):
        self.timer += seconds
        move = self.start + (self.timer * self.step)
        self.position[0] = move