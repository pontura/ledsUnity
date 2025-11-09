import urandom

class ExplotionParticle:
    def Init(self, numLeds, ledId, dir, color):
        self.ledId = ledId
        self.numLeds = numLeds
        self.Restart(ledId, dir, color)

    def Restart(self, ledId, dir, color):        
        self.speed = urandom.uniform(20, 220)
        self.color = 10
        self.oColor = color
        self.timer = 0
        self.isOn = True
        self.dir = dir
        self.ledId = ledId
        self.pos = ledId
        self.alpha = 0.9

    def OnUpdate(self, deltaTime):
        self.timer += deltaTime
        if self.timer > 0.25:
            self.color = self.oColor
        self.speed /= 1.1
        self.pos += deltaTime * self.speed * self.dir
        self.alpha -= deltaTime / (self.speed/50)
        if self.alpha < 0:
            self.isOn = False
            self.alpha = 0
            return

        self.ledId = int(self.pos)
        if self.ledId < 0:
            self.ledId = self.numLeds - 1 + self.ledId
        elif self.ledId >= self.numLeds:
            self.ledId = self.ledId - self.numLeds

        if self.timer > 1:
            self.isOn = False
