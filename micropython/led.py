class Led:
    id = 0
    trail_speed = 14
    value = 0
    curveValue = 0
    def Init(self, id):
        self.id = id
        self.value = 0
    def ChangeValues(self, value):
        self.value = value
    def Reset(self):
        if self.value > 0:
            if self.value > 1:
                self.value = self.value / self.trail_speed
            elif self.value < 1:
                self.value = 0
    def SetCurve(self, value):
        self.curveValue = value


