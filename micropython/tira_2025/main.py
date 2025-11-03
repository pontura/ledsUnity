import machine
import time
import character, shoots, enemies, audio, lightSignals
# import FPS
import leds
import intro, gameInit, fade
import automaticPlay
            
class BoublesGame:
    numLeds = 300
    chararter_width = 9
    myLeds = leds.Leds()
    lightSignals = lightSignals.LightSignals(14, 23)
    
    myLeds.Init(numLeds)
    audio = audio.Audio()
    intro = intro.Intro()
    automaticPlay = automaticPlay.AutomaticPlay()
    gameInit = gameInit.GameInit()
    fade = fade.Fade()
    ch = 1
    wonCh = 0
    deltaTime = 0.03
    centerColor = 0
    state = 5 #1=intro 2=game 5=fade
    
    def Init(self):
        self.delayToAdd = 0.4
        self.minDelayToAdd = 0.04
        self.speed = 0.001
#         self.delayToAdd = 0.1
#         self.minDelayToAdd = 0.002
#         self.speed = 0.1
        self.timeToAddColor = 25
        self.totalColors = 3
        self.seconds = 0
        self.timer = 0
        self.centerLedID = self.numLeds // 2
        self.audio.Init()

    def Start(self):
        self.Init()
        self.colors = [1,2,3,4,5,6]
        self.enemies = enemies.Enemies()
        
        #self.enemies.Init(self, self.chararter_width, self.numLeds)
        self.enemies.Init(self, 0, self.numLeds)
        
        self.intro.Init(self, self.numLeds)
        self.gameInit.Init(self, self.numLeds)
        self.automaticPlay.Init(self)
        self.fade.Init(self, self.numLeds)
        
        self.shoots = shoots.Shoots()
        self.shoots.Init(self, self.numLeds)
        self.characters = []

        ch = character.Character()
        ch.Init(self, 1, self.numLeds - 1, self.chararter_width, self.totalColors)
        self.characters.append(ch)
        
        ch = character.Character()
        ch.Init(self, 2, 0, self.chararter_width, self.totalColors)
        self.characters.append(ch)

        #self.from_range = self.chararter_width
        #self.to_range = self.numLeds - self.chararter_width        
        self.from_range = 0
        self.to_range = self.numLeds
        
        
        self.ledsData = [0] * self.numLeds

        self.Restart()
        self.Fade(1, 10)
        
    def Fade(self, gotoNext, color):
        self.GotoState(5)
        self.fade.InitFade(gotoNext, color)
        
    def Update(self):
        if self.state == 1: #intro
            self.intro.OnUpdate()
            self.lightSignals.Late() 
        elif self.state == 2:   #game         
            self.OnUpdate()
        elif self.state == 3:   #gameInit         
            self.gameInit.OnUpdate()
        elif self.state == 4:        #automatic    
            self.automaticPlay.OnUpdate()
            self.OnUpdate()
        elif self.state == 5:        #fade    
            self.fade.OnUpdate()
            
        self.myLeds.Send()
#         self.DrawDebug()
#         fps.Update()
    def InitGame(self):
        self.lightSignals.White()
        self.gameInit.Restart()
        self.GotoState(3)
        
    def Shoot(self, characterID : int):
        if self.state == 1:
            self.InitGame()
            return
        if self.state == 4: #automatic
            self.InitGame()
            return
        if self.enemies.state == 3:
            return
        self.audio.Fire(characterID)
        self.DoShoot(characterID)
        
    def DoShoot(self, characterID : int):
        ch = self.characters[characterID - 1]
        ledID = ch.ledId
       # if characterID == 1:
       #     ledID -= self.chararter_width
       # else:
       #     ledID += self.chararter_width
        self.shoots.AddBullet(characterID, ledID, ch.color)
        self.DoChangeColors(characterID, False)

    def ChangeColors(self, characterID, playSound : bool ):
        if self.state == 1:
            self.InitGame()
            return
        if self.state == 4:
            self.InitGame()
            return
        if self.enemies.state == 3:
            return 
        self.DoChangeColors(characterID, playSound)
        
    def DoChangeColors(self, characterID, playSound : bool):
        color = self.characters[characterID - 1].ChangeColors()
        if(playSound):            
            self.audio.Swap(characterID, color) 

    def Win(self, ch):
        self.lightSignals.Win(ch)
        self.wonCh = ch
        self.enemies.GameOver(ch)
        self.timer = 0

    def AddExplotion(self, from_range, to_range, characterID, color):
        self.audio.Explote(characterID)
        self.shoots.AddExplotion(from_range, to_range, characterID, color)

    def CollideWith(self, color, characterID):
        self.enemies.CollideWith(color, characterID)

    def OnReward(self, characterID, reward):
        print("OnReward", characterID)
        
    def Wrong(self, ch : int):        
        self.audio.Wrong(ch)

    def Restart(self):
        print("RESTART")
        self.Init()
        self.characters[0].Restart()
        self.characters[1].Restart()
        self.enemies.Restart()
        self.shoots.Restart()

    ch = 1
    chTick = 1
    
    def OnUpdate(self):
         
        self.UpdateCenter(self.deltaTime)
        if self.state != 4:
            self.audio.OnUpdate(self.deltaTime)
        
        self.seconds += self.deltaTime
        self.timer += self.deltaTime
        
        
        if self.enemies.state == 0:
            self.lightSignals.UpdateGame()
            self.enemies.CleanLeds(self.centerLedID, self.from_range, self.to_range, self.ch, self.characters[self.ch-1].color)
            
            if self.timer > self.delayToAdd:
                if self.delayToAdd < self.minDelayToAdd:
                    self.delayToAdd = self.minDelayToAdd
                else:
                    self.delayToAdd -= self.speed

                if self.seconds > self.timeToAddColor:
                    if self.totalColors < len(self.colors) - 1:
                        self.totalColors += 1
                    self.seconds = 0
                self.timer = 0
                
                if self.chTick == 1:
                    self.chTick = 2
                else:
                    self.chTick = 1                    
                    self.audio.Tick(self.chTick)
                
                #self.characters[1].Draw(self.numLeds)
                #self.characters[0].Draw(self.numLeds)
                
                self.enemies.UpdateDraw(self.chTick, self.centerLedID)
                
            
        elif self.enemies.state == 3: #3: dead!
            #if self.timer>0.5:
            if self.enemies.animState > 0:
                if self.wonCh == 1 and self.centerLedID>0:
                    self.centerLedID = self.centerLedID-2
                elif  self.centerLedID < self.numLeds-2:
                    self.centerLedID = self.centerLedID+2
#                 self.enemies.AnimDead(deltaTime, self.centerLedID, self.wonCh, False)
#             else:
            self.enemies.AnimDead(self.deltaTime, self.centerLedID, self.wonCh, True)
            self.enemies.CleanLeds(self.centerLedID, self.from_range, self.to_range, self.ch, 0)      

        else:
            self.enemies.AnimHit()
            self.timer = self.delayToAdd                    
        
        if self.ch == 1:
            self.ch = 2
        else:
            self.ch = 1
        if self.enemies.state != 3:
            self.shoots.OnUpdate(self.centerLedID, len(self.enemies.data), len(self.enemies.data2), self.deltaTime)
        
            
    
    def UpdateCenter(self, deltaTime):
        self.centerColor = self.centerColor+1
        if self.centerColor>self.totalColors:
            self.centerColor = 0
            
        if self.centerLedID+1<self.numLeds:
            self.SetLed(self.centerLedID+1, self.centerColor)        
        if self.centerLedID-1>0:
            self.SetLed(self.centerLedID-1, self.centerColor)
        self.SetLed(self.centerLedID, 0)
        
        
    def LoopNote(self, note : float, ch : int):
        self.audio.LoopNote(note, ch)
    
    #@micropython.viper 
    def SetCharacterColor(self, l :int , c :int):
        color = self.myLeds.GetColorReal(c)
        if l==1:
            self.lightSignals.SetCharacter1(color)
        else:
            self.lightSignals.SetCharacter2(color)
        
    @micropython.viper 
    def SetLed(self, l :int , c :int):        
        self.myLeds.SetLed(c, l)
        
    @micropython.viper 
    def SetLed2(self, l :int , c:int):
        self.myLeds.SetLed2(c, l)
        
    def SetLedColor(self, l :int , c:int):
        self.myLeds.SetLedColor(l,c)
            
    def SetLedAlpha(self, l :int , c:int , a = 0):
        self.myLeds.SetLedAlpha(int(c), l, a)      
        
    def GotoState(self, state : int):
        self.Restart()
        self.state = state
        print("New state", self.state)        
        self.audio.Stop(1)        
        self.audio.Stop(2)
        if state == 1:
            self.lightSignals.Off()
            
        
    def Match(self, characterID : int):

        if characterID == 1:
            if self.characters[0].color == self.enemies.currentColor:
                return True
        else:
            if self.characters[1].color == self.enemies.currentColor2:
                return True
        return False
        
        
    
        

game = BoublesGame()
game.Start()

ch1_b1 = machine.Pin(12, machine.Pin.IN, machine.Pin.PULL_UP )
ch1_b1_pressed = False
ch2_b1 = machine.Pin(19, machine.Pin.IN, machine.Pin.PULL_UP )
ch2_b1_pressed = False
ch1_b2 = machine.Pin(9, machine.Pin.IN, machine.Pin.PULL_UP )
ch1_b2_pressed = False
ch2_b2 = machine.Pin(22, machine.Pin.IN, machine.Pin.PULL_UP )
ch2_b2_pressed = False

# fps = FPS.fps()

def tt():
    return float(round(time.time() * 1000))

bfilter = 1
b1=0
b2=0
b3=0
b4=0

while True:
    if ch1_b1.value() == 1 and ch1_b1_pressed == False:
        if b1>bfilter:
            game.Shoot(1)
            ch1_b1_pressed = True
        b1 = 0        
    elif ch1_b1.value() == 0 and ch1_b1_pressed == True:
        ch1_b1_pressed = False
    elif ch1_b1.value() == 0 and ch1_b1_pressed == False:
        b1 = b1+1
        
        
    if ch2_b1.value() == 1 and ch2_b1_pressed == False:
        if b2>bfilter:
            game.Shoot(2)
            ch2_b1_pressed = True
        b2 = 0
    elif ch2_b1.value() == 0 and ch2_b1_pressed == True:        
        ch2_b1_pressed = False
    elif ch2_b1.value() == 0 and ch2_b1_pressed == False:
        b2 = b2+1
        
        
        
    if ch1_b2.value() == 1 and ch1_b2_pressed == False:
        if b3>bfilter:
            game.ChangeColors(1, True)     
            ch1_b2_pressed = True
        b3 = 0
    elif ch1_b2.value() == 0 and ch1_b2_pressed == True:        
        ch1_b2_pressed = False
    elif ch1_b2.value() == 0 and ch1_b2_pressed == False:
        b3 = b3+1
        
    if ch2_b2.value() == 1 and ch2_b2_pressed == False:
        if b4>bfilter:
            game.ChangeColors(2, True)
            ch2_b2_pressed = True
        b4 = 0
    elif ch2_b2.value() == 0 and ch2_b2_pressed == True:        
        ch2_b2_pressed = False
    elif ch2_b2.value() == 0 and ch2_b2_pressed == False:
        b4 = b4+1
        
    game.Update()
#     time.sleep(0.02)




