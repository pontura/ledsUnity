import math, enemy, random, settings, smoothPixel, trail
import utils

class Boss:
    fade = 0.0
    ledID = 0
    color = 1
    timer = 0
    delay_to_spawn = 1
    enemies = []
    pos = 0
    speed = 0.1
    smoothPixel = smoothPixel.SmoothPixel()
    trail = trail.Trail()
    
    def Init(self, _ledID, _color : int):
        self.ledID = _ledID
        self.color = _color
        self.trail.Init(_color, 10)

    def OnUpdate(self, deltaTime):
        self.timer = self.timer + deltaTime
        if self.timer > self.delay_to_spawn:
            c = 2
            if random.randrange(0,10) < 5:
                c = 3
            s = float( random.randrange(2,8) / 10)
            if random.randrange(0,10) < 5:
                s = s * -1
            self.AddEnemy(c, s)
            self.timer = 0
        l = len(self.enemies)
        for a in range(l):
            e = self.enemies[a]
            if e.IsAvailable():
                e.OnUpdate()
        
        self.Move(self.speed)        
        self.trail.Move(self.ledID, self.speed, deltaTime)
            
    def AddEnemy(self, color :int, speed : float):
        l = len(self.enemies)
        for a in range(l):
            e = self.enemies[a]
            print ("is available", e.IsAvailable())
            if e.IsAvailable() == False:
                e.Init(e._id, self.ledID, color, speed)
                return
                
        e = enemy.Enemy()
        e.Init(len(self.enemies), self.ledID, color, speed)
        self.enemies.append(e)
        
    def KillEnemy(self, _id : int):
        e = self.enemies[_id]
        e.Die()
        
    
    @micropython.viper    
    def Move(self, _speed):
        self.pos = self.pos + self.speed
        self.pos = utils.GetPos(self.pos)        
        self.smoothPixel.Set(self.ledID, self.pos, self.speed)
        self.ledID = math.floor(self.pos)
        
    



