import urandom
import machine
import time
import character, shoots, enemies
            
class BoublesGame:
    numLeds = 150
    chararter_width = 10
    
    def Init(self):
        self.delayToAdd = 0.5
        self.minDelayToAdd = 0.1
        self.speed = 0.0025
        self.timeToAddColor = 15
        self.totalColors = 3
        self.seconds = 0
        self.timer = 0
        self.centerLedID = self.numLeds // 2

    def Start(self):
        self.Init()
        self.colors = [1,2,3,4,5,6]
        self.enemies = enemies.Enemies()
        self.enemies.Init(self, self.chararter_width, self.numLeds)
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

    def Update(self, deltaTime):
        self.OnUpdate(deltaTime)
        self.characters[0].Draw(self.numLeds)
        self.characters[1].Draw(self.numLeds)
        self.SendData()

    def Shoot(self, characterID):
        ch = self.characters[characterID - 1]
        ledID = ch.ledId
        if characterID == 1:
            ledID -= 10
        else:
            ledID += 10
        self.shoots.AddBullet(characterID, ledID, ch.color)
        self.ChangeColors(characterID)

    def ChangeColors(self, characterID):
        self.characters[characterID - 1].ChangeColors()

    def Win(self, characterID):
        self.Restart()

    def AddExplotion(self, from_range, to_range, characterID, color):
        self.shoots.AddExplotion(from_range, to_range, characterID, color)

    def CollideWith(self, color, characterID):
        self.enemies.CollideWith(color, characterID)

    def OnReward(self, characterID, reward):
        if characterID == 1:
            self.centerLedID -= reward
        else:
            self.centerLedID += reward

    def Restart(self):
        self.Init()
        self.enemies.Restart()
        self.shoots.Restart()

    def OnUpdate(self, deltaTime):
        self.seconds += deltaTime
        self.timer += deltaTime

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

            self.enemies.UpdateDraw(self.centerLedID)

        self.enemies.CleanLeds(self.centerLedID, self.from_range, self.to_range)
        self.shoots.OnUpdate(self.centerLedID, len(self.enemies.data), len(self.enemies.data2), deltaTime)
    
    def SendData(self):
        s = ""
        for val in self.ledsData:
            s = s + str(val)
        print(s)
        

game = BoublesGame()
game.Start()

ch1_b1 = machine.Pin(15, machine.Pin.IN, machine.Pin.PULL_UP )
ch1_b1_pressed = False
ch2_b1 = machine.Pin(14, machine.Pin.IN, machine.Pin.PULL_UP )
ch2_b1_pressed = False

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
        
    game.Update(0.03)
    time.sleep(0.03)


