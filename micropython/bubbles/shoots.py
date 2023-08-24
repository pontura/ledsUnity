import explotion, bullet

class Shoots:
    def Init(self, game, numLeds):
        self.game = game
        self.explotions = []
        self.bullets = []
        self.numLeds = numLeds
        self.delayToAdd = 3
        self.timer = 0

    def Restart(self):
        self.explotions = []
        self.bullets = []

    def OnUpdate(self, centerLedID, data1Count, data2Count, deltaTime):
        for e in self.explotions:
            if e.isOn:
                e.OnUpdate(deltaTime)
                if e.isOn:
                    c = e.color
                    self.game.SetLed(e.ledId, c, e.alpha)
#                     self.game.ledsData[e.ledId] = c+e.alpha

        max_data1 = data1Count + centerLedID
        max_data2 = centerLedID - data2Count
        for e in self.bullets:
            color = e.color
            if e.isOn:
                e.OnUpdate(deltaTime)
                if e.isOn:
                    for l in e.leds:
                        if (e.characterID == 1 and l <= max_data1) or (e.characterID == 2 and l >= max_data2):
                            self.game.CollideWith(color, e.characterID)
                            e.Collide()
                            return
                        else:
                            self.game.SetLed(l, color)
#                             self.game.ledsData[l] = self.game.colors[color]

    def AddBullet(self, characterID, ledID, color):
        for b in self.bullets:
            if not b.isOn:
                b.Restart(characterID, ledID, color)
                return
        e = bullet.Bullet()
        e.Init(self, characterID, self.numLeds, ledID, color)
        self.bullets.append(e)

    def AddExplotion(self, from_range, to_range, characterID, color):        
        for a in range(from_range, to_range):
            self.AddExplotionParticle(a, characterID, color)

    def AddExplotionParticle(self, ledID, characterID, color):
        dir = 1 if characterID == 1 else -1
        c = self.game.colors[color]
        for ex in self.explotions:
            if not ex.isOn:
                ex.Restart(ledID, dir, c)
                return
        e = explotion.ExplotionParticle()
        e.Init(self.numLeds, ledID, dir, c)
        self.explotions.append(e)
