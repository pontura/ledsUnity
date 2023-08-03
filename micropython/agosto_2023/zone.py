import utils, math

class Zone:
    ledID = 0
    w = 0
    speed = 0.2
    pos = 0.0
    
    def Init(self, _ledID, w : int):
        self.w = w
        self.value = 1.0
        self.ledID = _ledID
        self.pos = _ledID

    def Move(self, deltaTime):       
        self.pos = utils.GetPos(self.pos - self.speed)
        self.ledID = math.floor(self.pos)

    def IsAvailable(self):
        if self.value <= 0:
            return True
        return False



