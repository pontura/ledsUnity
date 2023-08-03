import urandom

class ExplotionParticle:
    def Init(self, numLeds, ledId, dir, color):
        self.speed = urandom.uniform(20, 80)
        self.ledId = ledId
        self.numLeds = numLeds
        self.color = color
        self.Restart(ledId, dir, color)

    def Restart(self, ledId, dir, color):
        self.color = color
        self.timer = 0
        self.isOn = True
        self.dir = dir
        self.speed /= 1.01
        self.ledId = ledId
        self.pos = ledId
        self.alpha = 1

    def OnUpdate(self, deltaTime):
        self.timer += deltaTime
        self.speed /= 1.01
        self.pos += deltaTime * self.speed * self.dir
        self.alpha -= deltaTime / 2
        if self.alpha < 0:
            self.alpha = 0

        self.ledId = int(self.pos)
        if self.ledId < 0:
            self.ledId = self.numLeds - 1 + self.ledId
        elif self.ledId >= self.numLeds:
            self.ledId = self.ledId - self.numLeds

        if self.timer > 1:
            self.isOn = False
