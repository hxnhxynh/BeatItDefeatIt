from utils import SoundManager
from . import Drawable

class Interpolated(Drawable):
    def __init__(self, start, stop, bpm=60, fileName=""):
        super().__init__(start, fileName, (0,0))
        self.fileName = fileName
        self.start = start[0]
        self.stop = stop[0]
        self.bpm = bpm
        self.seconds = 4/(bpm/60)
        self.beat = self.seconds/4
        self.diff = self.stop-self.start
        self.timer = 0
        self.secTimer = 0
        self.play = False

    def update(self, seconds):
        self.timer += seconds
        self.secTimer += seconds
        if self.play and self.secTimer > self.beat:
            self.secTimer -= self.beat
            sm = SoundManager.getInstance()
            sm.playSFX("click.wav")
        if self.timer > self.seconds:
            self.timer -= self.seconds
        percentage = self.timer/self.seconds
        move = (percentage*self.diff) + self.start
        self.position[0] = move

       
            