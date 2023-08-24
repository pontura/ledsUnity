import urandom
import machine
import time
import character, shoots, enemies, audio
import FPS
import leds
# from neopixel import Neopixel

# deltaTime = 0.03
            
class BoublesGame:
#     numLeds = 300
    numLeds = 300
    chararter_width = 10
    myLeds = leds.Leds()
    audio = audio.Audio()
    ch = 1
    wonCh = 0
    deltaTime = 0.03
    
#     strip = Neopixel(numLeds, 0, 22, "RGBW")
#     strip.brightness(42)
    
    red = (255, 0, 0)
    orange = (255, 165, 0)
    yellow = (255, 150, 0)
    green = (0, 255, 0)
    blue = (0, 0, 255)
    indigo = (75, 0, 130)
    violet = (138, 43, 226)
    colors_rgb = (red, orange, yellow, green, blue, indigo, violet)
    
    def Init(self):
        self.myLeds.Init()
        self.delayToAdd = 0.25
        self.minDelayToAdd = 0.04
        self.speed = 0.002
#         self.delayToAdd = 0.1
#         self.minDelayToAdd = 0.002
#         self.speed = 0.1
        self.timeToAddColor = 15
        self.totalColors = 3
        self.seconds = 0
        self.timer = 0
        self.centerLedID = self.numLeds // 2

    def Start(self):
        self.Init()
        self.colors = [1,2,3,4,5,6]
        self.enemies = enemies.Enemies()
        self.enemies.Init(self, self.chararter_width, self.numLeds, self.colors)
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

    @micropython.viper 
    def Update(self):
        self.OnUpdate()
        self.characters[0].Draw(self.numLeds)
        self.characters[1].Draw(self.numLeds)
        self.SendData()

    def Shoot(self, characterID : int):
        if self.enemies.state == 3:
            return
        self.audio.Fire()
        ch = self.characters[characterID - 1]
        ledID = ch.ledId
        if characterID == 1:
            ledID -= 10
        else:
            ledID += 10
        self.shoots.AddBullet(characterID, ledID, ch.color)
        self.ChangeColors(characterID, False)

    def ChangeColors(self, characterID, playSound : bool ):
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
        self.enemies.Restart()
        self.shoots.Restart()

    ch = 1
    
    def OnUpdate(self):
        
        self.audio.OnUpdate(self.deltaTime)
        
        self.seconds += self.deltaTime
        self.timer += self.deltaTime
        
        
        if self.enemies.state == 0:
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
                if self.ch == 1:
                    self.ch = 2
                else:
                    self.ch = 1
                    self.audio.Tick()
                self.enemies.UpdateDraw(self.ch, self.centerLedID)
        elif self.enemies.state == 3: #3: dead!
            #if self.timer>0.5:
            if self.wonCh == 1 and self.centerLedID>0:
                self.centerLedID = self.centerLedID-1
            elif  self.centerLedID < self.numLeds-2:
                self.centerLedID = self.centerLedID+1
#                 self.enemies.AnimDead(deltaTime, self.centerLedID, self.wonCh, False)
#             else:
            self.enemies.AnimDead(self.deltaTime, self.centerLedID, self.wonCh, True)
                

        else:
            self.enemies.AnimHit()
            self.timer = self.delayToAdd
                    
        self.enemies.CleanLeds(self.centerLedID, self.from_range, self.to_range, self.ch, 0)
        
        if self.enemies.state != 3:
            self.shoots.OnUpdate(self.centerLedID, len(self.enemies.data), len(self.enemies.data2), self.deltaTime)
            
            
    def LoopNote(self, note : float):
        self.audio.LoopNote(note)
    
    @micropython.viper 
    def SendData(self):
        fps.Update()
#         self.strip.show()
#         self.DrawLeds()
#        self.DrawDebug()
        self.myLeds.Send()

    def SetLed(self, l, c, a = 0):
        a = c-int(c)
        if a>0:
            self.myLeds.SetLedAlpha(int(c), l, a)
        else:
            self.myLeds.SetLed(c, l)
        
    def DrawDebug(self):
        s = "".join(str(int(n)) for n in self.ledsData)
        print(s)
        

game = BoublesGame()
game.Start()

ch1_b1 = machine.Pin(15, machine.Pin.IN, machine.Pin.PULL_UP )
ch1_b1_pressed = False
ch2_b1 = machine.Pin(14, machine.Pin.IN, machine.Pin.PULL_UP )
ch2_b1_pressed = False
ch1_b2 = machine.Pin(13, machine.Pin.IN, machine.Pin.PULL_UP )
ch1_b2_pressed = False
ch2_b2 = machine.Pin(12, machine.Pin.IN, machine.Pin.PULL_UP )
ch2_b2_pressed = False

fps = FPS.fps()
    
while True:
    if ch1_b1.value() == 0 and ch1_b1_pressed == False:
        game.Shoot(1)
        ch1_b1_pressed = True
    elif ch1_b1.value() == 1 and ch1_b1_pressed == True:        
        ch1_b1_pressed = False
        
    if ch2_b1.value() == 0 and ch2_b1_pressed == False:
        game.Shoot(2)
        ch2_b1_pressed = True
    elif ch2_b1.value() == 1 and ch2_b1_pressed == True:        
        ch2_b1_pressed = False
        
    if ch1_b2.value() == 0 and ch1_b2_pressed == False:
        game.ChangeColors(1, True)     
        ch1_b2_pressed = True
    elif ch1_b2.value() == 1 and ch1_b2_pressed == True:        
        ch1_b2_pressed = False
        
    if ch2_b2.value() == 0 and ch2_b2_pressed == False:
        game.ChangeColors(2, True)
        ch2_b2_pressed = True
    elif ch2_b2.value() == 1 and ch2_b2_pressed == True:        
        ch2_b2_pressed = False
        

    game.Update()
    #time.sleep(0.03)



