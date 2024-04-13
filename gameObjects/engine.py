import pygame
from . import Drawable, Sequence, TimingBar, Player, NPC, Hitbox, Dialogue, Animated
from utils import vec, RESOLUTION, rectAdd, SCALE, SoundManager, WORLD_SIZE
from time import time

NUMARROWS = 5
SEQUENCE_SIZE = vec(32*NUMARROWS, 32)


class IntroEngine(object):
    import pygame

    def __init__(self):       
        self.size = vec(*RESOLUTION)
        self.back = False
        self.complete = False

        self.font1 =  pygame.font.SysFont("Harlow Solid", 15)
        self.font2 = pygame.font.SysFont("Arial Black", 15)

        self.slides = ["Intro1.png", "Intro2.png", "Intro3.png", "Intro4.png", "Intro5.png"]
        self.slideNum = 0
        self.background = Drawable((0,0), "Intro1.png")
        self.position = vec(0,0)
        self.slide = False

        self.transition = pygame.Surface(list(map(int, RESOLUTION))) 
        self.alpha = 255
        self.transition.set_alpha(255)                
        self.transition.fill((0,0,0))    

        self.next = self.font2.render("Next", False, (255, 255, 255))     
        
    
    def draw(self, drawSurface): 
        if self.background.getSize()[0] == RESOLUTION[0]:
            self.slide = False
        else:
            self.slide = True

        self.background.draw(drawSurface)

        drawSurface.blit(self.next, (530, 270))
        self.nextHitBox = rectAdd((530, 270), self.next.get_rect())
        drawSurface.blit(self.transition, (0,0))
        

    def handleEvent(self, event):
        if self.nextHitBox.collidepoint(vec(*pygame.mouse.get_pos())//SCALE):
            self.next = self.font2.render("Next", False, (0, 0, 0))
            if event.type == pygame.MOUSEBUTTONDOWN:
                self.slideNum += 1
                if self.slideNum == len(self.slides)-1:
                    self.complete = True
                
                self.background = Drawable((0,0), self.slides[self.slideNum])  
                self.alpha = 255    
                self.position = vec(0,0)   
        else:
            self.next = self.font2.render("Next", False, (255, 255, 255))
        
    
    def update(self, seconds):
        self.alpha -= 1
        if self.alpha < 0:
            self.alpha = 0
        self.transition.set_alpha(self.alpha) 

        if self.slide:
            self.position[0] -= 1
            if self.position[0] <= -600:
                self.background = Drawable((-600,0), self.slides[self.slideNum])
            else:
                self.background = Drawable((self.position[0],0), self.slides[self.slideNum])
        else:
            self.background = Drawable((0,0), self.slides[self.slideNum])


class Map(object):
    import pygame

    def __init__(self):
        self.size = vec(*RESOLUTION)
        self.background = Animated((0,0), "map.png")
        self.background.nFrames = 2
        self.background.framesPerSecond = 4
        self.area = "map"
        self.transition = False
        self.goTo = None

        self.LL = Hitbox((425,91), 136, 91)
        self.RS = Hitbox((295, 109), 106, 126)
        self.DK = Hitbox((52, 39), 171, 121)

        self.dkUnlocked = False

    def draw(self, drawSurface):
        self.background.draw(drawSurface)
        #self.LL.draw(drawSurface)
        #self.RS.draw(drawSurface)
        #self.DK.draw(drawSurface)

    def handleEvent(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            LL = self.LL.getRect()
            RS = self.RS.getRect()
            DK = self.DK.getRect()

            position = vec(*pygame.mouse.get_pos())//SCALE

            if LL.collidepoint(position):
                self.transition = True
                self.goTo = "lizLounge"
                #print("LL")
            elif RS.collidepoint(position):
                self.transition = True
                self.goTo = "ratShack"
                #print("RS")
            elif DK.collidepoint(position) and self.dkUnlocked:
                self.transition = True
                self.goTo = "dasKlub"
                #print("DK")

    def update(self, seconds):
        self.background.update(seconds)

class Ending(object):
    import pygame

    def __init__(self):
        self.size = vec(*RESOLUTION)
        self.background = Drawable((0,0), "ending.png")
        self.area = "ending"
        self.transition = False
        self.goTo = None
        self.readyToBattle = False
        self.battleDone = False

    def draw(self, drawSurface):
        self.background.draw(drawSurface)

    def handleEvent(self, event):
        pass

    def update(self, seconds):
        pass

class DasKlub(object):
    import pygame

    def __init__(self):
        self.size = vec(*RESOLUTION)
        self.background = Drawable((0,0), "dasKlubOff.png")
        self.area = "dasKlub"
        self.transition = False
        self.goTo = None
        self.readyToBattle = False
        self.battleDone = False

        self.player = Player((0,190),head=True)
        self.LK = Animated((460, 190-38), "lautstarK.png")
        self.LK.nFrames = 4
        self.LK.framesPerSecond = 4

        self.readyToTalk = False
        self.talking = False
        self.dialogues = [Dialogue("I see you've come for me.", begin="K",color = (76, 65, 100)),
                          Dialogue("Let us not waste any time.", begin="K",color = (76, 65, 100)),
                          Dialogue("!!!", begin="P", end="K",color = (76, 65, 100)),
                          Dialogue("DJ...turn the lights on.", begin="K",color = (76, 65, 100)),
                          Dialogue("Oh wait! That's me!", begin="K",color = (76, 65, 100)),
                          Dialogue("...", begin="P", end="K",color = (76, 65, 100))]
        self.dialogue = self.dialogues[0]

        self.currentTalk = 0
        self.bubble = Drawable((460, 120), "bubbles.png", (0,0))

        self.lkHit = Hitbox(self.LK.position-(30,0), 134, 86)
        self.playerHit = Hitbox(self.player.position, 48, 48)

        self.leaveBubble = Drawable((0,138), "upDown.png", (2,0))
        self.leaveBox = Hitbox((0,200), 100, 100)
        self.readyToLeave = False

    def draw(self, drawSurface):
        self.background.draw(drawSurface)
        self.LK.draw(drawSurface)
        #self.lkHit.draw(drawSurface)

        if self.readyToTalk:
            self.bubble.draw(drawSurface)

        if self.readyToLeave:
            self.leaveBubble.draw(drawSurface)

        self.player.draw(drawSurface)
        #self.playerHit.draw(drawSurface)

        if self.talking:
            self.dialogue.draw(drawSurface)
        
    def handleEvent(self, event):
        playerRect = self.playerHit.getRect()
        lkRect = self.lkHit.getRect()
        leaveRect = self.leaveBox.getRect()

        if playerRect.colliderect(lkRect):
            self.readyToTalk = True

            if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                self.talking = True
        else:
            self.readyToTalk = False
            self.talking = False

     
        if playerRect.colliderect(leaveRect):
            self.readyToLeave = True

            if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                self.transition = True
                self.goTo = "map"
        else:
            self.readyToLeave = False
        
        if self.talking:
            result = self.dialogue.handleEvent(event)
            if result:
                if self.battleDone:
                    self.talking = False
                else:
                    self.currentTalk += 1
                    if self.currentTalk >= len(self.dialogues):
                        self.transition = True
                        self.readyToBattle = True
                        self.talking = False
                        self.battleDone = True
                        self.player = Player(self.player.position, head=True)
                    else:
                        self.dialogue = self.dialogues[self.currentTalk]
        else:
            self.player.handleEvent(event)

    def update(self, seconds):
        self.player.update(seconds)
        self.LK.update(seconds)
        Drawable.updateOffset(self.player, self.size)

        self.playerHit.update(self.player.position)

class DasBattle(object):
    import pygame

    def __init__(self):
        self.paused = False   
        self.complete = False 
        self.transition = False
        self.size = vec(*RESOLUTION)
        self.readyToBattle = False
        self.finish = False

        self.player = Animated((120,190), "playerHead.png")
        self.player.framesPerSecond = 2
        self.player.nFrames = 4

        self.LK = Animated((460, 190-38), "lautstarK.png")
        self.LK.nFrames = 4
        self.LK.framesPerSecond = 4

        self.background = Drawable((0,0), "dasKlubBackground.png")
        self.lLight = Drawable((0,10), "LLLights1.png")
        self.rLight = Drawable((0,0), "LLLights2.png")
        
        self.area = "dasKlub"
        self.transition = False
        self.goTo = None

        self.font1 =  pygame.font.SysFont("Harlow Solid", 15)
        self.font2 = pygame.font.SysFont("Arial Black", 15)
        
        self.playerTurn = True

        self.sequence = Sequence(((RESOLUTION/2)-(SEQUENCE_SIZE[0]/2,-40)),
                                  NUMARROWS)
        self.timingBar = TimingBar(((RESOLUTION/2)-(SEQUENCE_SIZE[0]/2,0)), 92)
        self.points = 0
        self.pointDisplay = self.font1.render("Score count: 0",
                                             False,
                                             (255,255,255))
        #self.instructions = self.font1.render("Press the arrow keys in order to earn points!", False, (255,255,255))
        self.scoreNotifs = {"bad" : self.font2.render("Bad! +100 points", 
                                                     False, 
                                                     (245, 245, 245)),
                            "good": self.font2.render("Good job! +300 points",
                                                     False,
                                                     (0, 255, 255)),
                            "great": self.font2.render("Great job! +500 points",
                                                      False,
                                                      (0, 255, 0)),
                            "perf": self.font2.render("Perfect! +1000 points", 
                                                     False,
                                                     (255, 0, 255)),
                            "miss": self.font2.render("Miss! -100 points",
                                                      False,
                                                      (245, 245, 245))
                            }
        
        self.timer = 0
        self.waitingForBeats = True
        
        self.bubbles = [Drawable((435,120), "ouch.png", (0,2)),
                        Drawable((435,120), "ouch.png", (1,2)),
                        Drawable((435,120), "ouch.png", (2,2)),
                        Drawable((435,120), "ouch.png", (3,2)),
                        Drawable((435,120), "ouch.png", (4,2)),
                        Drawable((435,120), "ouch.png", (5,2)),
                        Drawable((435,120), "ouch.png", (6,2)),
                        ]
        self.bubble = self.bubbles[0]
    
    def draw(self, drawSurface):
        if self.finish:
            pass
        else:
            self.background.draw(drawSurface)
            self.LK.draw(drawSurface)
            self.player.draw(drawSurface)

        
            if self.playerTurn:
                #self.lLight.draw(drawSurface)
                if self.timer >= 2.5:
                    self.sequence.draw(drawSurface)
                    self.timingBar.draw(drawSurface)
                    scoreType =  self.timingBar.scoreType
                    if scoreType != None:
                        scoreNotif = self.scoreNotifs[scoreType]
                        drawSurface.blit(scoreNotif, (RESOLUTION[0]/2-(scoreNotif.get_width()//2), RESOLUTION[1]-70))
            
            if self.timer >= 5:
                self.bubble.draw(drawSurface)
                

            drawSurface.blit(self.pointDisplay, (0,280))
        
    def handleEvent(self, event):
        if self.finish:
            pass
        else:
            self.sequence.handleEvent(event)
            self.timingBar.handleEvent(event)
            if event.type == pygame.KEYDOWN and event.key == pygame.K_t:
                sm = SoundManager.getInstance()
                sm.fadeoutBGM()
                self.complete = True
                self.transition = True
                self.goTo = "ending"
            if self.sequence.complete:
                if self.timingBar.complete: # if sequence is completed and space bar is hit
                    self.timingBar.complete = False
                    self.sequence = Sequence(((RESOLUTION/2)-(SEQUENCE_SIZE[0]/2,-40)),NUMARROWS)
                    # increase and display points
                    self.points += self.timingBar.score 
                    self.pointDisplay = self.font1.render("Score count: " + str(self.points),
                                                        False,
                                                        (255,255,255)) 
                    sm = SoundManager.getInstance()
                    sm.playSFX("slap.wav")       
            else:
                if self.timingBar.complete:
                    self.timingBar.complete = False
                        
                    # penalty for pressing space bar w/o completing sequence
                    self.points -= 100
                    self.timingBar.scoreType = "miss"
                    self.pointDisplay = self.font1.render("Score count: " + str(self.points),
                                                        False,
                                                        (255,255,255))  
 

    def update(self, seconds):
        if self.finish:
            pass
        else:
            self.player.update(seconds)
            self.LK.update(seconds)

            self.timer += seconds

            if self.waitingForBeats:
                if self.timer >= .66:
                    self.waitingForBeats = False
                    #self.timingBar.bar.play = True
                    sm = SoundManager.getInstance()
                    sm.playBGM("Techno 120 BPM.mp3")
            
            self.timingBar.update(seconds)
                

            if self.timer >=23 and self.timer < 32:
                self.bubble = self.bubbles[1]
            elif self.timer >= 32 and self.timer < 40:
                self.bubble = self.bubbles[2]
            elif self.timer >=40 and self.timer <50:
                self.bubble = self.bubbles[3]
            elif self.timer >=50 and self.timer <69:
                self.bubble = self.bubbles[4]
            elif self.timer >=69 and self.timer <80:
                self.bubble = self.bubbles[5]
            elif self.timer >=80 and self.timer <90:
                self.bubble = self.bubbles[6]
            elif self.timer >= 120:
                sm = SoundManager.getInstance()
                sm.fadeoutBGM()
                self.complete = True
                self.transition = True
                self.goTo = "ending"

class RatShack(object):
    import pygame

    def __init__(self):
        self.size = vec(*RESOLUTION)
        self.background = Drawable((0,0), "ratShack.png")
        self.area = "ratShack"
        self.transition = False
        self.goTo = None
        self.readyToBattle = False
        self.battleDone = False

        self.player = Player((0,190))
        self.ladyB = Animated((460, 190-38), "ladyB.png")
        self.ladyB.nFrames = 4
        self.ladyB.framesPerSecond = 4

        self.readyToTalk = False
        self.talking = False
        self.dialogues = [Dialogue("Howdy...\nI hear you're the lil fella that\ntook out ol' boy Smooth.", begin="B", 
                                 color = (76, 65, 100)),
                                 Dialogue("...", end="B", begin="P",
                                 color = (76, 65, 100)),
                                 Dialogue("Not a big talker, are we?\nAnd humble too!", begin="B", 
                                 color = (76, 65, 100)),
                                 Dialogue("...", end="B", begin="P",
                                 color = (76, 65, 100)),
                                 Dialogue("OK, shy guy! The name's Beatrice.\nLady Beatrice to you.", begin="B", 
                                 color = (76, 65, 100)),
                                 Dialogue("..!", end="B", begin="P",
                                 color = (76, 65, 100)),
                                 Dialogue("That's right, I'm the one who runs\nthings 'round here.", begin="B", 
                                 color = (76, 65, 100)),
                                 Dialogue("...", end="B", begin="P",
                                 color = (76, 65, 100)),
                                 Dialogue("Yes, the things in question are\nour friday night line dances...", begin="B", 
                                 color = (76, 65, 100)),
                                 Dialogue("It's hard to move up the ladder\nhere!", begin="B", 
                                 color = (76, 65, 100)),
                                 Dialogue("...", end="B", begin="P",
                                 color = (76, 65, 100)),
                                 Dialogue("The economy is rough!", begin="B", 
                                 color = (76, 65, 100)),
                                 Dialogue("...", end="B", begin="P",
                                 color = (76, 65, 100)),
                                 Dialogue("I'm just a girl!", begin="B", 
                                 color = (76, 65, 100)),
                                 Dialogue("..?", end="B", begin="P",
                                 color = (76, 65, 100)),
                                 Dialogue("OK, lady robot girl. Dun' matter!", begin="B", 
                                 color = (76, 65, 100)),
                                 Dialogue("...", end="B", begin="P",
                                 color = (76, 65, 100)),
                                 Dialogue("Whatever. We have more in common\nthan you think.", begin="B", 
                                 color = (76, 65, 100)),
                                 Dialogue("This city is different now...\nIt wun' like this before...", begin="B", 
                                 color = (76, 65, 100)),
                                 Dialogue("People used to dance, sing, and\nmake music.Now all they do is hit\nsome buttons on a keypad and call\nit music!", begin="B", 
                                 color = (76, 65, 100)),
                                 Dialogue("...", end="B", begin="P",
                                 color = (76, 65, 100)),
                                 Dialogue("Just because I'm a robot dun' mean\nI like techno!", begin="B", 
                                 color = (76, 65, 100)),
                                 Dialogue("...", end="B", begin="P",
                                 color = (76, 65, 100)),
                                 Dialogue("Anyways, the culture has been\ndifferent. Ever since that lil'\DJ boy came in town.", begin="B", 
                                 color = (76, 65, 100)),
                                 Dialogue("..!", end="B", begin="P",
                                 color = (76, 65, 100)),
                                 Dialogue("Of course, you know him.\nEveryone's a Lautstar-K fan nowadays.\nI can't stand it!", begin="B", 
                                 color = (76, 65, 100)),
                                 Dialogue("..?", end="B", begin="P",
                                 color = (76, 65, 100)),
                                 Dialogue("Das Klub used to play club bangers!\nThey had a rotation of new DJs\nweekly...\nThey don't do that now...", begin="B", 
                                 color = (76, 65, 100)),
                                 Dialogue("..?", end="B", begin="P",
                                 color = (76, 65, 100)),
                                 Dialogue("Some people think they\ndeserve to shine more than others...\nIt's a DJ monopoly!", begin="B", 
                                 color = (76, 65, 100)),
                                 Dialogue("So many newcomers like you come\ninto town....And then they get their\ndreams crushed...", begin="B", 
                                 color = (76, 65, 100)),
                                 Dialogue("Sell the big Arcadian dream...\nThat's how Mr.Smooth gets his lil'\nworkers!", begin="B", 
                                 color = (76, 65, 100)),
                                 Dialogue("...", end="B", begin="P",
                                 color = (76, 65, 100)),
                                 Dialogue("Sorry to hit a nerve...\nYou've got real potential...", begin="B", 
                                 color = (76, 65, 100)),
                                 Dialogue("Wait...\nMaybe you can be the one to take\nthem all down.", begin="B", 
                                 color = (76, 65, 100)),
                                 Dialogue("..?", end="B", begin="P",
                                 color = (76, 65, 100)),
                                 Dialogue("Yup, you! If you defeat me in a\nrhythm battle, I'll give you\nsomething special.", begin="B", 
                                 color = (76, 65, 100)),
                                 Dialogue("!!!", end="B", begin="P",
                                 color = (76, 65, 100)),
                                 Dialogue("A pair of magical headphones.\nIt'll protect you from Lautstar-k's\nmega-speakers.", begin="B", 
                                 color = (76, 65, 100)),
                                 Dialogue("..?", end="B", begin="P",
                                 color = (76, 65, 100)),
                                 Dialogue("You know you're doing it.\nNow let's get training!", begin="B", 
                                 color = (76, 65, 100)),
        ]
        self.dialogue = self.dialogues[0]
        self.afterBattle = Dialogue("Get your booty to Das Klub now, boy!", begin="B", 
                                 color = (76, 65, 100))
        self.currentTalk = 0
        self.bubble = Drawable((460, 120), "bubbles.png", (0,0))

        self.ladyHit = Hitbox(self.ladyB.position-(30,0), 134, 86)
        self.playerHit = Hitbox(self.player.position, 48, 48)

        self.leaveBubble = Drawable((0,138), "upDown.png", (2,0))
        self.leaveBox = Hitbox((0,200), 100, 100)
        self.readyToLeave = False


    def draw(self, drawSurface):
        self.background.draw(drawSurface)
        self.ladyB.draw(drawSurface)
        #self.ladyHit.draw(drawSurface)

        if self.readyToTalk:
            self.bubble.draw(drawSurface)

        if self.readyToLeave:
            self.leaveBubble.draw(drawSurface)

        self.player.draw(drawSurface)
        #self.playerHit.draw(drawSurface)

        if self.talking:
            self.dialogue.draw(drawSurface)

    def handleEvent(self, event):
        playerRect = self.playerHit.getRect()
        ladyRect = self.ladyHit.getRect()
        leaveRect = self.leaveBox.getRect()

        if playerRect.colliderect(ladyRect):
            self.readyToTalk = True

            if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                self.talking = True
        else:
            self.readyToTalk = False
            self.talking = False

     
        if playerRect.colliderect(leaveRect):
            self.readyToLeave = True

            if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                self.transition = True
                self.goTo = "map"
        else:
            self.readyToLeave = False
        
        if self.talking:
            result = self.dialogue.handleEvent(event)
            if result:
                if self.battleDone:
                    self.talking = False
                else:
                    self.currentTalk += 1
                    if self.currentTalk >= len(self.dialogues):
                        self.transition = True
                        self.readyToBattle = True
                        self.talking = False
                        self.dialogue = self.afterBattle
                        self.battleDone = True
                        self.player = Player(self.player.position, head=True)
                    else:
                        self.dialogue = self.dialogues[self.currentTalk]
        else:
            self.player.handleEvent(event)

    def update(self, seconds):
        self.player.update(seconds)
        self.ladyB.update(seconds)
        Drawable.updateOffset(self.player, self.size)

        self.playerHit.update(self.player.position)

class RatBattle(object):
    import pygame

    def __init__(self):
        self.paused = False   
        self.complete = False 
        self.transition = False
        self.size = vec(*RESOLUTION)
        self.readyToBattle = False

        self.player = Animated((120,190), "playerSheet.png")
        self.player.framesPerSecond = 2
        self.player.nFrames = 4

        self.ladyB = Animated((460, 190-38), "ladyB.png")
        self.ladyB.nFrames = 4
        self.ladyB.framesPerSecond = 4

        self.background = Drawable((0,0), "ratShack.png")
        self.lLight = Drawable((0,0), "LLLights1.png")
        self.rLight = Drawable((0,0), "LLLights2.png")
        
        self.area = "ratShack"
        self.transition = False
        self.goTo = None

        self.font1 =  pygame.font.SysFont("Harlow Solid", 15)
        self.font2 = pygame.font.SysFont("Arial Black", 15)
        
        self.playerTurn = True

        self.sequence = Sequence(((RESOLUTION/2)-(SEQUENCE_SIZE[0]/2,-40)),
                                  NUMARROWS)
        self.timingBar = TimingBar(((RESOLUTION/2)-(SEQUENCE_SIZE[0]/2,0)), 92)
        self.points = 0
        self.pointDisplay = self.font1.render("Score count: 0",
                                             False,
                                             (255,255,255))
        #self.instructions = self.font1.render("Press the arrow keys in order to earn points!", False, (255,255,255))
        self.scoreNotifs = {"bad" : self.font2.render("Bad! +100 points", 
                                                     False, 
                                                     (245, 245, 245)),
                            "good": self.font2.render("Good job! +300 points",
                                                     False,
                                                     (0, 255, 255)),
                            "great": self.font2.render("Great job! +500 points",
                                                      False,
                                                      (0, 255, 0)),
                            "perf": self.font2.render("Perfect! +1000 points", 
                                                     False,
                                                     (255, 0, 255)),
                            "miss": self.font2.render("Miss! -100 points",
                                                      False,
                                                      (245, 245, 245))
                            }
        
        self.timer = 0
        self.waitingForBeats = True
        
        self.bubbles = [Drawable((435,120), "ouch.png", (0,1)),
                        Drawable((435,120), "ouch.png", (1,1)),
                        Drawable((435,120), "ouch.png", (2,1)),
                        Drawable((435,120), "ouch.png", (3,1)),
                        Drawable((435,120), "ouch.png", (4,1)),
                        Drawable((435,120), "ouch.png", (5,1)),
                        Drawable((435,120), "ouch.png", (6,1)),
                        ]
        self.bubble = self.bubbles[0]
    
    def draw(self, drawSurface):
        self.background.draw(drawSurface)
        self.ladyB.draw(drawSurface)
        self.player.draw(drawSurface)

    
        if self.playerTurn:
            #self.lLight.draw(drawSurface)
            if self.timer >= 2.5:
                self.sequence.draw(drawSurface)
                self.timingBar.draw(drawSurface)
                scoreType =  self.timingBar.scoreType
                if scoreType != None:
                    scoreNotif = self.scoreNotifs[scoreType]
                    drawSurface.blit(scoreNotif, (RESOLUTION[0]/2-(scoreNotif.get_width()//2), RESOLUTION[1]-70))
        
        if self.timer >= 5:
            self.bubble.draw(drawSurface)
            

        drawSurface.blit(self.pointDisplay, (0,280))
        
    def handleEvent(self, event):
        self.sequence.handleEvent(event)
        self.timingBar.handleEvent(event)
        if event.type == pygame.KEYDOWN and event.key == pygame.K_t:
            sm = SoundManager.getInstance()
            sm.fadeoutBGM()
            self.complete = True
            self.transition = True
            self.goTo = "ratShack"
        if self.sequence.complete:
            if self.timingBar.complete: # if sequence is completed and space bar is hit
                self.timingBar.complete = False
                self.sequence = Sequence(((RESOLUTION/2)-(SEQUENCE_SIZE[0]/2,-40)),NUMARROWS)
                # increase and display points
                self.points += self.timingBar.score 
                self.pointDisplay = self.font1.render("Score count: " + str(self.points),
                                                    False,
                                                    (255,255,255)) 
                sm = SoundManager.getInstance()
                sm.playSFX("bloop.wav")       
        else:
            if self.timingBar.complete:
                self.timingBar.complete = False
                    
                # penalty for pressing space bar w/o completing sequence
                self.points -= 100
                self.timingBar.scoreType = "miss"
                self.pointDisplay = self.font1.render("Score count: " + str(self.points),
                                                    False,
                                                    (255,255,255))
 

    def update(self, seconds):
        self.player.update(seconds)
        self.ladyB.update(seconds)

        self.timer += seconds

        if self.waitingForBeats:
            if self.timer >= .66:
                self.waitingForBeats = False
                #self.timingBar.bar.play = True
                sm = SoundManager.getInstance()
                sm.playBGM("Country 90 BPM.mp3")
        
        self.timingBar.update(seconds)
            

        if self.timer >=23 and self.timer < 32:
            self.bubble = self.bubbles[1]
        elif self.timer >= 32 and self.timer < 40:
            self.bubble = self.bubbles[2]
        elif self.timer >=40 and self.timer <50:
            self.bubble = self.bubbles[3]
        elif self.timer >=50 and self.timer <69:
            self.bubble = self.bubbles[4]
        elif self.timer >=69 and self.timer <80:
            self.bubble = self.bubbles[5]
        elif self.timer >=80 and self.timer <90:
            self.bubble = self.bubbles[6]
        elif self.timer >= 90:
            sm = SoundManager.getInstance()
            sm.fadeoutBGM()
            self.complete = True
            self.transition = True
            self.goTo = "ratShack"


class LizLoungeEngine(object):
    import pygame

    def __init__(self):       
        self.size = vec(*WORLD_SIZE)
        self.background = Drawable((0,0), "lizardLounge.png")
        self.stage = Drawable((0,0), "background.png")
        self.player = Player((0,246))
        self.NPC = NPC((200, 246))
        self.area = "lizLounge"
        self.transition = False
        self.goTo = None
        self.readyToBattle = False

        self.readyToTalk = False
        self.talking = False
        self.dialogues = [Dialogue("Hey buddy...\nTry to avoid the tables near the\nstage. He's in a mood.", 
                                 color = (76, 65, 100)),
                                 Dialogue("Why Mr. Smooth always gotta be such\na Mr. Snappy?", 
                                 color = (76, 65, 100))]
        self.dialogue = self.dialogues[0]
        self.currentTalk = 0
        self.bubble = Drawable((204, 215), "bubbles.png", (0,0))

        self.hitboxes = [Hitbox(self.NPC.position-(26, 0), 100, 48),]
        self.playerHit = Hitbox(self.player.position, 48, 48)
        
        self.hitPos = [self.NPC.position-(26, 0)]
        self.stageBox = Hitbox((900, 200), 100,100)
        self.upBubble = Drawable((900, 200), "upDown.png", (0,0))
        self.leaveBubble = Drawable((0,200), "upDown.png", (2,0))
        self.leaveBox = Hitbox((0,200), 100, 100)

        self.canGoUp = False
        self.readyToLeave = False
        self.canLeave = False
    
        
    def draw(self, drawSurface):     
        self.background.draw(drawSurface)
        self.NPC.draw(drawSurface)
        
        #for hitbox in self.hitboxes:
        #    hitbox.draw(drawSurface)
        
        #self.playerHit.draw(drawSurface)

        #self.stageBox.draw(drawSurface)

        if self.readyToTalk:
            self.bubble.draw(drawSurface)

        if self.canGoUp:
            self.upBubble.draw(drawSurface)

        if self.readyToLeave:
            self.leaveBubble.draw(drawSurface)

        self.player.draw(drawSurface)

        if self.talking:
            self.dialogue.draw(drawSurface)


    def handleEvent(self, event):
        playerRect = self.playerHit.getRect()
        npcRect = self.hitboxes[0].getRect()
        stageRect = self.stageBox.getRect()
        leaveRect = self.leaveBox.getRect()

        if playerRect.colliderect(npcRect):
            self.readyToTalk = True

            if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                self.talking = True
        else:
            self.readyToTalk = False
            self.talking = False

        if playerRect.colliderect(stageRect):
            self.canGoUp = True

            if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                self.transition = True
                self.goTo = "lizStage"
        else:
            self.canGoUp = False

        if self.canLeave: 
            if playerRect.colliderect(leaveRect):
                self.readyToLeave = True

                if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                    self.transition = True
                    self.goTo = "map"
        
        if self.talking:
            result = self.dialogue.handleEvent(event)
            if result:
                self.currentTalk += 1
                if self.currentTalk >= len(self.dialogues):
                    self.talking = False
                    self.currentTalk = 0
                    self.dialogue = self.dialogues[0]
                else:
                    self.dialogue = self.dialogues[self.currentTalk]
        else:
            self.player.handleEvent(event)
        
    
    def update(self, seconds):
        self.player.update(seconds)
        self.NPC.update(seconds)
        Drawable.updateOffset(self.player, self.size)
        for i in range(len(self.hitboxes)):
            self.hitboxes[i].update(self.hitPos[i])

        self.playerHit.update(self.player.position)
        self.stageBox.update(self.stageBox.position)
        self.leaveBox.update(self.leaveBox.position)
        
class LizStageEngine(object):
    import pygame

    def __init__(self):
        self.size = vec(*RESOLUTION)
        self.player = Player((530,190))
        self.Mr = Animated((100, 144),"mrSmooth.png")
        self.Mr.nFrames = 4
        self.Mr.framesPerSecond = 4
        self.background = Drawable((0,0), "lizardLoungeStage.png")
        self.lights = Drawable((0,0), "lizardLoungeStageLights.png")
        self.area = "lizStage"
        self.transition = False
        self.goTo = None
        self.readyToBattle = False
        self.battleDone = False

        self.readyToTalk = False
        self.talking = False
        self.beforeBattle = [Dialogue("What are you looking at, idiot?", begin="L", end="P",
                                 color = (76, 65, 100)),
                                 Dialogue("...", begin="P", end="L",
                                 color = (76, 65, 100)),
                                 Dialogue("Your buddy down there has been\nslacking all week!", begin="L", end="P",
                                 color = (76, 65, 100)),
                                 Dialogue("...?", begin="P", end="L",
                                 color = (76, 65, 100)),
                                 Dialogue("What? He says he's been cleaning \nthe shot glasses twice a night with\ndegreaser and steel wool?", begin="L", end="P",
                                 color = (76, 65, 100)),
                                 Dialogue("...", begin="P", end="L",
                                 color = (76, 65, 100)),
                                 Dialogue("...", begin="L", end="P",
                                 color = (76, 65, 100)),
                                 Dialogue("...", begin="P", end="L",
                                 color = (76, 65, 100)),
                                 Dialogue("YOU THINK YOU KNOW BETTER THAN ME?!", begin="L", end="P",
                                 color = (76, 65, 100)),
                                 Dialogue("...", begin="P", end="L",
                                 color = (76, 65, 100)),
                                 Dialogue("What? You think you’re Mr. Funny?\nMr. Cool Guy? Mr. Smooth even?!", begin="L", end="P",
                                 color = (76, 65, 100)),
                                 Dialogue("...", begin="P", end="L",
                                 color = (76, 65, 100)),
                                 Dialogue("WELL YOU'RE NOT! DON'T PISS ME OFF!", begin="L", end="P",
                                 color = (76, 65, 100)),
                                 Dialogue("...", begin="P", end="L",
                                 color = (76, 65, 100)),
                                 Dialogue("!!!", begin="P", end="L",
                                 color = (76, 65, 100)),
                                 Dialogue("YOU WANT TO CHALLENGE ME TO A\nRHYTHM BATTLE? ARE YOU NUTS?!", begin="L", end="P",
                                 color = (76, 65, 100)),
                                 Dialogue("!!!", begin="P", end="L",
                                 color = (76, 65, 100)),
                                 Dialogue("Oh, you're serious.", begin="L", end="P",
                                 color = (76, 65, 100)),
                                 Dialogue("OK. Prepare to DIE!!!!", begin="L", end="P",
                                 color = (76, 65, 100)),
                                 ]
        self.afterBattle = Dialogue("Get out of my sight, kid.", begin="L", end="P", color = (76, 65, 100))
        self.dialogue = self.beforeBattle[0]
        self.currentTalk = 0
        self.bubble = Drawable(self.Mr.position - (-35, 35), "bubbles.png", (0,0))

        self.hitboxes = [Hitbox(self.Mr.position, 130, 100),]
        self.hitPos = [self.Mr.position]
        self.playerHit = Hitbox(self.player.position, 48, 48)

        self.stageBox = Hitbox((500, 142), 100,100)
        self.downBubble = Drawable((500, 142), "upDown.png", (1,0))
        self.canGoDown = False

    def draw(self, drawSurface):
        self.background.draw(drawSurface)
        self.Mr.draw(drawSurface)
        #self.stageBox.draw(drawSurface)
        self.player.draw(drawSurface)

        #self.hitboxes[0].draw(drawSurface)
        #self.playerHit.draw(drawSurface)

        if self.readyToTalk:
            self.bubble.draw(drawSurface)

        if self.canGoDown:
            self.downBubble.draw(drawSurface)
        
        self.lights.draw(drawSurface)

        if self.talking:
            self.dialogue.draw(drawSurface)


    def handleEvent(self, event):
        playerRect = self.playerHit.getRect()
        mrRect = self.hitboxes[0].getRect()
        stageRect = self.stageBox.getRect()

        if playerRect.colliderect(mrRect):
            self.readyToTalk = True

            if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                self.talking = True
        else:
            self.readyToTalk = False
            self.talking = False

        if playerRect.colliderect(stageRect):
            self.canGoDown = True

            if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                self.transition = True
                self.goTo = "lizLounge"
        else:
            self.canGoDown = False
        
        if self.talking:

            result = self.dialogue.handleEvent(event)
            if result:
                if self.battleDone:
                    self.talking = False
                else:
                    self.currentTalk += 1
                    if self.currentTalk >= len(self.beforeBattle):
                        self.transition = True
                        self.readyToBattle = True
                        self.talking = False
                        self.dialogue = self.afterBattle
                        self.battleDone = True
                    else:
                        self.dialogue = self.beforeBattle[self.currentTalk]
        else:
            self.player.handleEvent(event)

    def update(self, seconds):
        self.player.update(seconds)
        self.Mr.update(seconds)
        Drawable.updateOffset(self.player, self.size)
        
        for i in range(len(self.hitboxes)):
            self.hitboxes[i].update(self.hitPos[i])

        self.playerHit.update(self.player.position)

class LizBattle(object):
    import pygame

    def __init__(self):
        self.paused = False   
        self.complete = False 
        self.transition = False
        self.size = vec(*RESOLUTION)
        self.readyToBattle = False

        self.player = Animated((450,190), "playerSheet.png")
        self.player.framesPerSecond = 2
        self.player.nFrames = 4
        self.player.flipImage[0] = True

        self.Mr = Animated((100, 144),"mrSmooth.png")
        self.Mr.nFrames = 4
        self.Mr.framesPerSecond = 4

        self.background = Drawable((0,0), "lizardLoungeStage.png")
        self.lLight = Drawable((0,0), "LLLights1.png")
        self.rLight = Drawable((0,0), "LLLights2.png")
        
        self.area = "lizStage"
        self.transition = False
        self.goTo = None
        
        self.playerTurn = True

        self.font1 =  pygame.font.SysFont("Harlow Solid", 15)
        self.font2 = pygame.font.SysFont("Arial Black", 15)

        self.box = Drawable((0,0), "instructions.png")
        self.start = False
        self.step1 = self.font2.render("1. Press the keys in order.", False, (255, 255, 255))
        self.step2 = self.font2.render("2. Press the space bar when reaching the middle of the CD.", False, (255, 255, 255))
        self.testSeq = Sequence(vec(50, 90), 5)
        self.testBar = TimingBar(vec(50, 197))
        self.ok = self.font2.render("Let's play!", False, (255, 255, 255))
        self.okHitBox = rectAdd((460, 250), self.ok.get_rect())

        self.sequence = Sequence(((RESOLUTION/2)-(SEQUENCE_SIZE[0]/2,-40)),
                                  NUMARROWS)
        self.timingBar = TimingBar(((RESOLUTION/2)-(SEQUENCE_SIZE[0]/2,0)), 60)
        self.points = 0
        self.pointDisplay = self.font1.render("Score count: 0",
                                             False,
                                             (255,255,255))
        #self.instructions = self.font1.render("Press the arrow keys in order to earn points!", False, (255,255,255))
        self.scoreNotifs = {"bad" : self.font2.render("Bad! +100 points", 
                                                     False, 
                                                     (245, 245, 245)),
                            "good": self.font2.render("Good job! +300 points",
                                                     False,
                                                     (0, 255, 255)),
                            "great": self.font2.render("Great job! +500 points",
                                                      False,
                                                      (0, 255, 0)),
                            "perf": self.font2.render("Perfect! +1000 points", 
                                                     False,
                                                     (255, 0, 255)),
                            "miss": self.font2.render("Miss! -100 points",
                                                      False,
                                                      (245, 245, 245))
                            }
        
        self.timer = 0
        self.waitingForBeats = True

        self.bubbles = [Drawable((100,100), "ouch.png", (0,0)),
                        Drawable((100,100), "ouch.png", (1,0)),
                        Drawable((100,100), "ouch.png", (2,0)),
                        Drawable((100,100), "ouch.png", (3,0)),
                        Drawable((100,100), "ouch.png", (4,0)),
                        Drawable((100,100), "ouch.png", (5,0)),
                        Drawable((100,100), "ouch.png", (6,0)),
                        ]
        self.bubble = self.bubbles[0]
    
    def draw(self, drawSurface):
        self.background.draw(drawSurface)
        self.Mr.draw(drawSurface)
        self.player.draw(drawSurface)

        if self.start:
            if self.playerTurn:
                self.rLight.draw(drawSurface)
                if self.timer >= 1.5:
                    self.sequence.draw(drawSurface)
                    self.timingBar.draw(drawSurface)
            if self.timer >= 5:
                self.bubble.draw(drawSurface)

            drawSurface.blit(self.pointDisplay, (0,280))
            scoreType =  self.timingBar.scoreType
            if scoreType != None:
                scoreNotif = self.scoreNotifs[scoreType]
                drawSurface.blit(scoreNotif, (RESOLUTION[0]/2-(scoreNotif.get_width()//2), RESOLUTION[1]-70))
        else:
            self.box.draw(drawSurface)

            drawSurface.blit(self.step1, (36, 67))
            drawSurface.blit(self.step2, (36, 167))

            self.testSeq.draw(drawSurface)
            self.testBar.draw(drawSurface)

            drawSurface.blit(self.ok, (480, 250))
        
    def handleEvent(self, event):
        if self.start:
            self.sequence.handleEvent(event)
            self.timingBar.handleEvent(event)
            if event.type == pygame.KEYDOWN and event.key == pygame.K_t:
                sm = SoundManager.getInstance()
                sm.fadeoutBGM()
                self.complete = True
                self.transition = True
                self.goTo = "lizStage"
            if self.sequence.complete:
                if self.timingBar.complete: # if sequence is completed and space bar is hit
                    self.timingBar.complete = False
                    self.sequence = Sequence(((RESOLUTION/2)-(SEQUENCE_SIZE[0]/2,-40)),NUMARROWS)
                    # increase and display points
                    self.points += self.timingBar.score 
                    self.pointDisplay = self.font1.render("Score count: " + str(self.points),
                                                        False,
                                                        (255,255,255)) 
                    sm = SoundManager.getInstance()
                    sm.playSFX("ouch.wav")       
            else:
                if self.timingBar.complete:
                    self.timingBar.complete = False
                    
                    # penalty for pressing space bar w/o completing sequence
                    self.points -= 100
                    self.timingBar.scoreType = "miss"
                    self.pointDisplay = self.font1.render("Score count: " + str(self.points),
                                                        False,
                                                        (255,255,255))
        else:
            if self.okHitBox.collidepoint(vec(*pygame.mouse.get_pos())//SCALE):
                self.ok = self.font2.render("Let's play!", False, (0, 0, 0))
                if event.type == pygame.MOUSEBUTTONDOWN:
                    self.start = True
                    sm = SoundManager.getInstance()
                    sm.playBGM("Jazz 120 BPM.mp3")
            else:
                self.ok = self.font2.render("Let's play!", False, (255, 255, 255))

    def update(self, seconds):
        if self.start:
            self.player.update(seconds)
            self.Mr.update(seconds)

            self.timer += seconds

            if self.waitingForBeats:
                if self.timer >= 1.5:
                    self.waitingForBeats = False
                    #self.timingBar.bar.play = True
            
            self.timingBar.update(seconds)
            

            if self.timer >=20 and self.timer < 33:
                self.bubble = self.bubbles[1]
            elif self.timer >= 33 and self.timer < 48:
                self.bubble = self.bubbles[2]
            elif self.timer >=48 and self.timer <61:
                self.bubble = self.bubbles[3]
            elif self.timer >=61 and self.timer <81:
                self.bubble = self.bubbles[4]
            elif self.timer >=81 and self.timer <90:
                self.bubble = self.bubbles[5]
            elif self.timer >=90 and self.timer <103:
                self.bubble = self.bubbles[6]
            elif self.timer >= 103:
                sm = SoundManager.getInstance()
                sm.fadeoutBGM()
                self.complete = True
                self.transition = True
                self.goTo = "lizStage"
            else:
                self.playerTurn = True

        else:
            self.testBar.update(seconds)

class TutorialEngine(object):
    import pygame

    def __init__(self):   
        self.paused = False   
        self.complete = False 
        self.transition = False
        self.size = vec(*RESOLUTION)
        self.background = Drawable((0,0), "dasKlubBackground.png")
        self.font1 =  pygame.font.SysFont("Harlow Solid", 15)
        self.font2 = pygame.font.SysFont("Arial Black", 15)

        self.box = Drawable((0,0), "instructions.png")
        self.start = False
        self.step1 = self.font2.render("1. Press the keys in order.", False, (255, 255, 255))
        self.step2 = self.font2.render("2. Press the space bar when reaching the middle of the CD.", False, (255, 255, 255))
        self.testSeq = Sequence(vec(50, 90), 5)
        self.testBar = TimingBar(vec(50, 197))
        self.ok = self.font2.render("Let's play!", False, (255, 255, 255))
        self.okHitBox = rectAdd((460, 250), self.ok.get_rect())
    
    def draw(self, drawSurface):        
        self.background.draw(drawSurface)
    
        self.box.draw(drawSurface)

        drawSurface.blit(self.step1, (36, 67))
        drawSurface.blit(self.step2, (36, 167))

        self.testSeq.draw(drawSurface)
        self.testBar.draw(drawSurface)

        drawSurface.blit(self.ok, (480, 250))
            

    def handleEvent(self, event):
        if self.okHitBox.collidepoint(vec(*pygame.mouse.get_pos())//SCALE):
            self.ok = self.font2.render("Let's play!", False, (0, 0, 0))
            if event.type == pygame.MOUSEBUTTONDOWN:
                self.complete = True
        else:
            self.ok = self.font2.render("Let's play!", False, (255, 255, 255))
    
    def update(self, seconds):
        if not self.paused:   
            self.testBar.update(seconds)


class TutGameEngine(object):
    import pygame

    def __init__(self):
        self.paused = False
        self.size = vec(*RESOLUTION)
        self.background = Drawable((0,0), "dasKlubBackground.png")
        self.font1 =  pygame.font.SysFont("Harlow Solid", 15)
        self.font2 = pygame.font.SysFont("Arial Black", 15)

        self.waitingForBeats = True
        self.waitingForMusic = True
        self.wait = 10
        self.timer = 0
        self.musicTimer = 0
        self.sequence = Sequence(((RESOLUTION/2)-(SEQUENCE_SIZE[0]/2,-40)),
                                  NUMARROWS)
        self.timingBar = TimingBar(((RESOLUTION/2)-(SEQUENCE_SIZE[0]/2,0)), 52)
        self.points = 0
        self.pointDisplay = self.font1.render("Score count: 0",
                                             False,
                                             (255,255,255))
        #self.instructions = self.font1.render("Press the arrow keys in order to earn points!", False, (255,255,255))
        self.scoreNotifs = {"bad" : self.font2.render("Bad! +100 points", 
                                                     False, 
                                                     (245, 245, 245)),
                            "good": self.font2.render("Good job! +300 points",
                                                     False,
                                                     (0, 255, 255)),
                            "great": self.font2.render("Great job! +500 points",
                                                      False,
                                                      (0, 255, 0)),
                            "perf": self.font2.render("Perfect! +1000 points", 
                                                     False,
                                                     (255, 0, 255)),
                            "miss": self.font2.render("Miss! -100 points",
                                                      False,
                                                      (245, 245, 245))
                            }
    
    
    def draw(self, drawSurface):
        self.background.draw(drawSurface)
        if not self.waitingForBeats:
            self.timingBar.draw(drawSurface)
            self.sequence.draw(drawSurface)

        #if self.waitingForBeats:
            #if self.timer >= self.wait:
                #self.waitingForBeats = False
                #self.timingBar.bar.play = True
                
        drawSurface.blit(self.pointDisplay, (0,0))
        scoreType =  self.timingBar.scoreType
        if scoreType != None:
            scoreNotif = self.scoreNotifs[scoreType]
            drawSurface.blit(scoreNotif, (RESOLUTION[0]/2-(scoreNotif.get_width()//2), RESOLUTION[1]-70))

    def handleEvent(self, event):
        self.sequence.handleEvent(event)
        self.timingBar.handleEvent(event)
        if self.sequence.complete:
            if self.timingBar.complete: # if sequence is completed and space bar is hit
                self.timingBar.complete = False
                self.sequence = Sequence(((RESOLUTION/2)-(SEQUENCE_SIZE[0]/2,-40)),NUMARROWS)
                # increase and display points
                self.points += self.timingBar.score 
                self.pointDisplay = self.font1.render("Score count: " + str(self.points),
                                                    False,
                                                    (255,255,255)) 
                self.counting = True         
        else:
            if self.timingBar.complete:
                self.timingBar.complete = False
                
                # penalty for pressing space bar w/o completing sequence
                self.points -= 100
                self.timingBar.scoreType = "miss"
                self.pointDisplay = self.font1.render("Score count: " + str(self.points),
                                                    False,
                                                    (255,255,255))
                
    def update(self, seconds):
        #if self.waitingForMusic:
            #self.musicTimer += seconds
                #self.waitingForMusic = False
                #sm = SoundManager.getInstance()
                #sm.playBGM("Disco  Drum Metronome Loop  60 BPM.mp3")
        if self.waitingForBeats:
            self.timer += seconds
            if self.timer >= 1.5:
                self.waitingForBeats = False
                #self.timingBar.bar.play = True
        else:
            self.timingBar.update(seconds)



