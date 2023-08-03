import utils

class SmoothPixel:
    value = 0.0
    ledID = 0
    def Set(self, _ledID : int, pos : float, speed : float):
        if(speed > 0):
            _ledID = _ledID+1
        else:                
            _ledID = _ledID-1
        self.ledID = utils.GetPos(_ledID)
        self.value = pos - int(pos)