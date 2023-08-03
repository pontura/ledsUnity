class Bullet:
    def Init(self, shoots, characterID, numLeds, ledId, color):
        self.characterID = characterID
        self.ledId = ledId
        self.width = 7
        self.color = color
        self.numLeds = numLeds
        self.shoots = shoots
        self.dir = 1 
        self.timer = 0
        self.leds = [0] * self.width
        self.isOn = True
        self.pos = ledId
        self.speed = 100.0

    def Restart(self, characterID, ledId, color):
        self.characterID = characterID
        self.color = color
        self.pos = ledId
        self.ledId = ledId
        self.timer = 0
        self.isOn = True

    def OnUpdate(self, deltaTime):
        if self.characterID == 1:
            self.pos -= deltaTime * self.speed
            if self.pos < 0:
                self.isOn = False
                return
        else:
            self.pos += deltaTime * self.speed
            if self.pos > self.numLeds - 1:
                self.isOn = False
                return

        self.ledId = int(self.pos)
        thisLed = self.ledId - int(self.width / 2)
        for i in range(self.width):
            if thisLed < 0:
                thisLed = self.numLeds + thisLed
            elif thisLed >= self.numLeds:
                thisLed = thisLed - self.numLeds
            self.leds[i] = thisLed
            thisLed += 1

    def Collide(self):
        self.isOn = False