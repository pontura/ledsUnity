import machine
import time
import character, shoots, enemies, audio
import FPS
import leds
import intro
# from neopixel import Neopixel

# deltaTime = 0.03
            
class BoublesGame:
#     numLeds = 300
    numLeds = 299
    chararter_width = 2
    myLeds = leds.Leds()
    audio = audio.Audio()
    intro = intro.Intro()
    ch = 1
    wonCh = 0
    deltaTime = 0.03
    centerColor = 0
    state = 1 #1=intro 2=game
    
#     strip = Neopixel(numLeds, 0, 22, "RGBW")
#     strip.brightness(42)
        
    def Init(self):
        self.myLeds.Init()
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

    def Start(self):
        self.Init()
        self.colors = [1,2,3,4,5,6]
        self.enemies = enemies.Enemies()
        self.enemies.Init(self, self.chararter_width, self.numLeds)
        self.intro.Init(self)
        self.shoots = shoots.Shoots()
        self.shoots.Init(self, self.numLeds)
        self.characters = []

        ch = character.Character()
        ch.Init(self, 1, self.numLeds - 1, self.chararter_width, self.totalColors)
        self.characters.append(ch)
        ch = character.Character()
        ch.Init(self, 2, 0, self.chararter_width, self.totalColors)
        self.characters.append(ch)

        self.from_range = self.chararter_width
        self.to_range = self.numLeds - self.chararter_width

        self.ledsData = [0] * self.numLeds

        self.Restart()

    def Update(self):        
        if self.state == 1:
            self.intro.OnUpdate()
        elif self.state == 2:            
            self.OnUpdate()

        self.myLeds.Send()
#        self.DrawDebug()
        fps.Update()

    def Shoot(self, characterID : int):
        if self.state == 1:
            print ("shoot", self.state)
            self.GotoState(2)
            return
        if self.enemies.state == 3:
            return
        self.audio.Fire()
        ch = self.characters[characterID - 1]
        ledID = ch.ledId
        if characterID == 1:
            ledID -= self.chararter_width
        else:
            ledID += self.chararter_width
        self.shoots.AddBullet(characterID, ledID, ch.color)
        self.ChangeColors(characterID, False)

    def ChangeColors(self, characterID, playSound : bool ):
        if self.state == 1:
            print ("ChangeColors", self.state)
            self.GotoState(2)
            return
        if self.enemies.state == 3:
            return
        if(playSound):            
            self.audio.Swap()   
        self.characters[characterID - 1].ChangeColors()

    def Win(self, ch):
        self.wonCh = ch
        self.enemies.GameOver(ch)
        self.timer = 0

    def AddExplotion(self, from_range, to_range, characterID, color):
        self.audio.Explote()
        self.shoots.AddExplotion(from_range, to_range, characterID, color)

    def CollideWith(self, color, characterID):
        self.enemies.CollideWith(color, characterID)

    def OnReward(self, characterID, reward):
        print("OnReward", characterID)
        
    def Wrong(self):        
        self.audio.Wrong()

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
        self.audio.OnUpdate(self.deltaTime)
        
        self.seconds += self.deltaTime
        self.timer += self.deltaTime
        
        
        if self.enemies.state == 0:
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
                    self.audio.Tick()
                self.enemies.UpdateDraw(self.chTick, self.centerLedID)
                
            self.characters[0].Draw(self.numLeds)
            self.characters[1].Draw(self.numLeds)
            
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
        self.SetLed(self.centerLedID, self.centerColor)
        
    def LoopNote(self, note : float):
        self.audio.LoopNote(note)
    
        
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
        
    def DrawDebug(self):
        s = "".join(str(int(n)) for n in self.ledsData)
        print(s)
        
    def GotoState(self, state : int):
        self.Restart()
        self.state = state
        print("New state", self.state)        
        self.audio.Stop()   
    
        

game = BoublesGame()
game.Start()

ch1_b1 = machine.Pin(15, machine.Pin.IN, machine.Pin.PULL_UP )
ch1_b1_pressed = False
ch2_b1 = machine.Pin(13, machine.Pin.IN, machine.Pin.PULL_UP )
ch2_b1_pressed = False
ch1_b2 = machine.Pin(14, machine.Pin.IN, machine.Pin.PULL_UP )
ch1_b2_pressed = False
ch2_b2 = machine.Pin(12, machine.Pin.IN, machine.Pin.PULL_UP )
ch2_b2_pressed = False

fps = FPS.fps()

def tt():
    return float(round(time.time() * 1000))
    
while True:
    if ch1_b1.value() == 1 and ch1_b1_pressed == False:
        game.Shoot(1)
        ch1_b1_pressed = True
    elif ch1_b1.value() == 0 and ch1_b1_pressed == True:
        ch1_b1_pressed = False        
    if ch2_b1.value() == 1 and ch2_b1_pressed == False:
        game.Shoot(2)
        ch2_b1_pressed = True
    elif ch2_b1.value() == 0 and ch2_b1_pressed == True:        
        ch2_b1_pressed = False
        ch1b = tt()
        
    if ch1_b2.value() == 1 and ch1_b2_pressed == False:
        game.ChangeColors(1, True)     
        ch1_b2_pressed = True
    elif ch1_b2.value() == 0 and ch1_b2_pressed == True:        
        ch1_b2_pressed = False        
    if ch2_b2.value() == 1 and ch2_b2_pressed == False:
        game.ChangeColors(2, True)
        ch2_b2_pressed = True
    elif ch2_b2.value() == 0 and ch2_b2_pressed == True:        
        ch2_b2_pressed = False
        
    game.Update()
    #time.sleep(0.03)



