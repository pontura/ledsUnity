int ledID;
float value;
float speed;
float direction;

def Init(_ledID, initialAlpha):
    self.value = initialAlpha;
    self.ledID = _ledID;

def SetSpeed(_speed, _direction)
    self.direction = _direction;
    self.speed = _speed;

def OnUpdate(deltaTime, fade_desaceleration)
    if (self.value == 0):
        return;
    self.value = self.value - (fade_desaceleration * deltaTime);
    if (self.value < 0):
        value = 0;

def IsAvailable()
    return value == 0;

