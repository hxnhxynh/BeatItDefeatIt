# Beat It Defeat It main program
# Author: Han Huynh

import pygame
from UI import ScreenManager
#from gameObjects import GameEngine
from utils import SpriteManager, RESOLUTION, UPSCALED

def main():
    #Initialize the module
    pygame.init()
    
    pygame.font.init()
    
    
    #Get the screen
    screen = pygame.display.set_mode(list(map(int, UPSCALED)))
    drawSurface = pygame.Surface(list(map(int, RESOLUTION)))
  
    gameEngine = ScreenManager()
    
    RUNNING = True
    
    while RUNNING:
        gameEngine.draw(drawSurface)
        
        pygame.transform.scale(drawSurface,
                               list(map(int, UPSCALED)),
                               screen)
     
        pygame.display.flip()
        gameClock = pygame.time.Clock()
        
        # event handling, gets all event from the eventqueue
        # handles events from event queue
        for event in pygame.event.get():
            # if quit action triggered...
            if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                # break out of loop!
                RUNNING = False
            else:
                result = gameEngine.handleEvent(event)

                if result == "exit":
                    RUNNING = False
        
        gameClock.tick(60)
        seconds = gameClock.get_time() / 1000
        gameEngine.update(seconds)
     
    pygame.quit()


if __name__ == '__main__':
    main()
