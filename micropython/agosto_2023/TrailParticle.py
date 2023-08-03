class TrailParticle:
    ledID = 0
    value = 10.0
    
    def Init(self, _ledID):
        self.value = 1.0
        self.ledID = _ledID

    def OnUpdate(self, deltaTime):
        if self.value == 0:
            return
        self.value = self.value - deltaTime
        if (self.value < 0):
            self.value = 0

    def IsAvailable(self):
        if self.value <= 0:
            return True
        return False


