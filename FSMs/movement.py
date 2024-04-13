from . import AbstractGameFSM
from utils import vec, magnitude

from statemachine import State

class MovementFSM(AbstractGameFSM):
    WORLD_SIZE = vec(1000,300)
    def update(self, seconds):
        
        for dim in range(2):
            if self.obj.position[dim] < 0:
                self.obj.velocity[dim] = max(self.obj.velocity[dim], 0)
            elif self.obj.position[dim] + self.obj.getSize()[dim] >= self.WORLD_SIZE[0]:
                self.obj.velocity[dim] = min(self.obj.velocity[dim], 0)
        


class AccelerationFSM(MovementFSM):
    """Axis-based acceleration with gradual stopping."""
    not_moving = State(initial=True)
    
    negative = State()
    positive = State()
    
    stalemate = State()
    
    decrease  = not_moving.to(negative) | negative.to.itself(internal=True) | \
                positive.to(stalemate)  | stalemate.to.itself(internal=True)
    
    increase = not_moving.to(positive) | positive.to.itself(internal=True) | \
               negative.to(stalemate)  | stalemate.to.itself(internal=True)
    
    stop_decrease = not_moving.to.itself(internal=True)  | positive.to.itself(internal=True) | \
                    negative.to(not_moving) | stalemate.to(positive)
    
    stop_increase = not_moving.to.itself(internal=True)  | negative.to.itself(internal=True) | \
                    positive.to(not_moving) | stalemate.to(negative)
    
    stop_all      = not_moving.to.itself(internal=True)  | negative.to(not_moving) | \
                    positive.to(not_moving) | stalemate.to(not_moving)
    
    def __init__(self, obj, axis=0):
        self.axis      = axis
        self.direction = vec(0,0)
        self.direction[self.axis] = 1
        self.accel = 200
        
        super().__init__(obj)

    def update(self, seconds=0):
        if self == "positive":
            self.obj.velocity += self.direction * self.accel * seconds
            if self.axis == 0:
                self.obj.flipImage[0] = False
        elif self == "negative":
            self.obj.velocity -= self.direction * self.accel * seconds
            if self.axis == 0:
                self.obj.flipImage[0] = True
                
        elif self == "stalemate":
            pass
        else:
            if self.obj.velocity[self.axis] > self.accel * seconds:
                self.obj.velocity[self.axis] -= self.accel * seconds
            elif self.obj.velocity[self.axis] < -self.accel * seconds:
                self.obj.velocity[self.axis] += self.accel * seconds
            else:
                self.obj.velocity[self.axis] = 0
        
        
    
        super().update(seconds)