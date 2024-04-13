from . import Animated

class NPC(Animated):
    
    def __init__(self, position):
        super().__init__(position, "playerSheet.png")
        self.nFrames = 4
        self.framesPerSecond = 4


    
    def update(self, seconds): 
      super().update(seconds)