import math
class Character:
    
    ledId = 0
    pos = 0.0
    color = (0,0,0)
    originalColor = (0,0,0)
    numLeds = 0
    speed = 0.0
    state = 0
    maxSpeed = 0.0
    dangerZoneMaxSpeed = 0.0
    originalSpeed = 0.0
    aceleration = 0.0
    #public Trail trail
    #1 move
    #2 in danger
    #3 crash

    def Init(numLeds, _ledID, _color, maxSpeed):    
        #self.trail = new Trail()
        #trail.Init()
        self.state = 1
        self.originalSpeed = maxSpeed
        self.dangerZoneMaxSpeed = maxSpeed / 2
        self.maxSpeed = maxSpeed 
        self.numLeds = numLeds
        self.originalColor = _color
        self.color = _color
        self.ledId = _ledID
        self.pos = _ledID
    
    def OnUpdate(_speed, deltaTime):
        #trail_fade_desaceleration = 500
        #trail.OnUpdate(deltaTime, (int)pos, trail_fade_desaceleration)
        if (self.state == 1 || self.state == 2):
            self.Move(_speed, deltaTime)
        else if (self.state == 3):
            self.CheckToBeBack()
    
    lastSpeed = 0
    def Move(_speed, deltaTime):    
        self.lastSpeed = self.lerp(self.lastSpeed, _speed*self.maxSpeed, deltaTime * 30)
        self.speed = self.lastSpeed
        if (state == 1):        
            self.pos = self.pos + speed
            if (self.pos >= self.numLeds) pos = 0
            else if (pos < 0) self.pos = self.numLeds - 1
            self.ledId = (int)self.pos
    

    def OutOfDanger():  
        self.color = self.originalColor
        self.maxSpeed = self.originalSpeed
        self.state = 1
        self.timer = 0
    
    timer = 0
    def InDangerZone(self, framerate):
        self.state = 2
        self.timer += framerate
        self.color = (255,255,255)
        self.maxSpeed = self.dangerZoneMaxSpeed
        if (self.timer > 0.5)
            self.Crash()
            
    def Crash(self):    
        color = Color.white
        state = 2
        speed = 0
    
    timeToRestart = 1
    def CheckToBeBack(self):
    
        timer += Time.deltaTime
        if (timer > timeToRestart)
            Restart()
    
    def Restart(self):    
        color = originalColor
        timer = 0
        state = 1
        speed = 0
        
    def lerp(a: float, b: float, t: float) -> float:
        return (1 - t) * a + t * b
    
