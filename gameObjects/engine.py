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

        self.canGoUp = False
    
        
    def draw(self, drawSurface):     
        self.background.draw(drawSurface)
        self.NPC.draw(drawSurface)
        self.player.draw(drawSurface)
        
        #for hitbox in self.hitboxes:
        #    hitbox.draw(drawSurface)
        
        #self.playerHit.draw(drawSurface)

        #self.stageBox.draw(drawSurface)

        if self.readyToTalk:
            self.bubble.draw(drawSurface)

        if self.canGoUp:
            self.upBubble.draw(drawSurface)

        if self.talking:
            self.dialogue.draw(drawSurface)




    def handleEvent(self, event):
        playerRect = self.playerHit.getRect()
        npcRect = self.hitboxes[0].getRect()
        stageRect = self.stageBox.getRect()

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
        self.beforeBattle = [Dialogue("What are you looking at, idiot?", 
                                 color = (76, 65, 100)),
                                 Dialogue("...", begin="p", end="L",
                                 color = (76, 65, 100)),
                                 Dialogue("Your buddy down there has been\nslacking all week!", 
                                 color = (76, 65, 100)),
                                 Dialogue("...?", begin="p", end="L",
                                 color = (76, 65, 100)),
                                 Dialogue("What? He says he's been cleaning \nthe shot glasses twice a night with\ndegreaser and steel wool?", 
                                 color = (76, 65, 100)),
                                 Dialogue("...", begin="p", end="L",
                                 color = (76, 65, 100)),
                                 Dialogue("...", 
                                 color = (76, 65, 100)),
                                 Dialogue("...", begin="p", end="L",
                                 color = (76, 65, 100)),
                                 Dialogue("YOU THINK YOU KNOW BETTER THAN ME?!", 
                                 color = (76, 65, 100)),
                                 Dialogue("...", begin="p", end="L",
                                 color = (76, 65, 100)),
                                 Dialogue("What? You think you’re Mr. Funny?\nMr. Cool Guy? Mr. Smooth even?!", 
                                 color = (76, 65, 100)),
                                 Dialogue("...", begin="p", end="L",
                                 color = (76, 65, 100)),
                                 Dialogue("WELL YOU'RE NOT! DON'T PISS ME OFF!", 
                                 color = (76, 65, 100)),
                                 Dialogue("...", begin="p", end="L",
                                 color = (76, 65, 100)),
                                 Dialogue("!!!", begin="p", end="L",
                                 color = (76, 65, 100)),
                                 Dialogue("YOU WANT TO CHALLENGE ME TO A\nRHYTHM BATTLE? ARE YOU NUTS?!", 
                                 color = (76, 65, 100)),
                                 Dialogue("!!!", begin="p", end="L",
                                 color = (76, 65, 100)),
                                 Dialogue("Oh, you're serious.", 
                                 color = (76, 65, 100)),
                                 Dialogue("OK. Prepare to DIE!!!!", 
                                 color = (76, 65, 100)),
                                 ]
        self.afterBattle = Dialogue("Get out of my sight, kid.", color = (76, 65, 100))
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
    
    def draw(self, drawSurface):
        self.background.draw(drawSurface)
        self.Mr.draw(drawSurface)
        self.player.draw(drawSurface)

        if self.start:
            if self.playerTurn:
                self.rLight.draw(drawSurface)
            else:
                self.lLight.draw(drawSurface)
        else:
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
                self.start = True
        else:
            self.ok = self.font2.render("Let's play!", False, (255, 255, 255))

    def update(self, seconds):
        if self.start:
            self.player.update(seconds)
            self.Mr.update(seconds)
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

        self.waitingForBeats = False
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
        if not self.waitingForMusic:
            self.timingBar.draw(drawSurface)
            self.sequence.draw(drawSurface)
            self.timingBar.bar.play = True
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
        if self.waitingForMusic:
            self.musicTimer += seconds
            if self.musicTimer > 7:
                self.waitingForMusic = False
                #sm = SoundManager.getInstance()
                #sm.playBGM("Disco  Drum Metronome Loop  60 BPM.mp3")
        #if self.waitingForBeats:
        #    self.timer += seconds

        if not self.waitingForMusic:
            self.timingBar.update(seconds)



