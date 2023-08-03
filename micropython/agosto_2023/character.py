import math, trail, utils, smoothPixel, trail

class Character:
    global leds
    global z
    inBoostZone = True
    ledId = 0
    lastLedID = 0
    pos = 0.0
    color = 3
    originalColor = (0,0,0)
    numLeds = 0
    speed = 0.1
    minSpeed = 0.1
    aceleration = 0.2
    state = 0
    des = 0.01
    smoothPixel = smoothPixel.SmoothPixel()
    trail = trail.Trail() 
    timerDead = 0
    
    def Init(self, _numLeds, _ledID, _color : int, _maxSpeed, leds, z):
        self.leds = leds
        self.z = z
        self.smoothPixel = smoothPixel.SmoothPixel()
        self.trail = trail.Trail() 
        self.numLeds = _numLeds
        self.originalColor = _color
        self.color = _color
        self.ledId = _ledID
        self.pos = _ledID        
        self.trail.Init(_color, 15, leds)
    
    def OnUpdate(self, boosted : True, deltaTime : float):
        if self.inBoostZone:
            self.color = 1
        else:
            self.color = 2
        if (self.state == 1):            
            self.Move(boosted, deltaTime)
            self.CheckCollision()
            self.lastLedID = self.ledId
        elif (self.state == 2):
            self.CheckToBeBack(deltaTime)
        elif (self.state == 0):
            if boosted:
                self.state = 1
        
        self.Draw(deltaTime)
        
    def Draw(self, deltaTime):
        self.trail.Move(self.ledId, self.speed, deltaTime)
        self.leds.AddAlpha(self.color, self.smoothPixel.ledID, self.smoothPixel.value)
        self.leds.Add(self.color, self.ledId)
                
    def Move(self, boosted, deltaTime):    
        self.pos = self.pos + self.speed
        self.pos = utils.GetPos(self.pos)            
        self.smoothPixel.Set(self.ledId, self.pos, self.speed)
        self.ledId = math.floor(self.pos)            
        if boosted:
            if self.inBoostZone:                
                self.speed = self.minSpeed
#                 self.state = 2
                self.timerDead = 0
            else:         
                self.speed = self.speed + self.aceleration
        else:
            self.speed = self.speed - self.des
            if self.speed <= self.minSpeed:
                self.speed = self.minSpeed
       
            
    def CheckCollision(self):
        self.EnterZone(self.z.CheckCollisionIn(self.ledId))
            
    def EnterZone(self, inBoost : bool):
        self.inBoostZone = inBoost
        
    def CheckToBeBack(self, deltaTime):
        self.timerDead = self.timerDead + deltaTime
        print ("____________", self.timerDead)
        if self.timerDead > 1:
            state = 1
    
    


