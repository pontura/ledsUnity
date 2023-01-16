import led
import explotion

class Character:
    # 0 = waiting
    # 1 = playing
    # 2 = explote
    # 3 = inDanger
    recovery = 0.02 #recovery acceleration from stopped
    speed = 0
    maxspeed = 1
    framerate = 3
    framerate_danger_zone = 0.5
    original_framerate = 3
    acceleration = 0.01
    state = 1 
    global explotion
    id = 0
    dead_timer = 0
    timer_to_reborn = 2
    reborn_speed = 0.03
    color = (255,0,0)
    
    def Init(self, id, framerate, acceleration):
        self.original_framerate = framerate
        self.framerate = framerate
        self.acceleration = acceleration
        self.id = id
        self.pos = 0
        if id == 1:
            self.color = (0,0,255)
        else:
            self.color = (0,255,0)
            
    def Reset(self):
        self.state = 1
        self.maxspeed = 1
        
    def Move(self, value, NUM_LEDS):
        if self.state == 1 or self.state == 3:
            if self.framerate<self.original_framerate:
                self.framerate = self.framerate + self.recovery          
                if self.framerate>self.original_framerate:
                    self.framerate = self.original_framerate
                    
            if self.speed < value:
                self.speed = self.speed + self.acceleration            
                if self.speed > self.maxspeed:
                    self.speed = self.maxspeed
            if self.speed > value:
                self.speed = self.speed - self.acceleration            
                if self.speed < 0:
                    self.speed = 0
            self.pos = self.pos + (self.speed*self.framerate)           
            if self.pos > NUM_LEDS:
                self.pos = 0
                
        elif self.state == 2:
            self.dead_timer = self.dead_timer + self.reborn_speed
            if self.dead_timer > self.timer_to_reborn:
                self.WakeUp()
        
            
    def Explote(self, NUM_PARTICLES):
        self.speed = 0
        self.state = 2
        thisExplotion = explotion.Explotion()
        thisExplotion.Init(round(self.pos), self.id, self.color, NUM_PARTICLES)
        self.dead_timer = 0
    def WakeUp(self):
        self.Reset()
        self.speed = 0
        self.state = 1
        
    inDangerDuration = 2
    inDangerTimer = 0
    
    def InDangerZone(self):        
#         print('InDangerZone ', self.inDangerTimer, ' self.state: ', self.state)
        if self.state == 1:
            self.framerate = self.framerate_danger_zone
            self.state = 3
            self.inDangerTimer = self.inDangerDuration
        elif self.state == 3:
            if self.inDangerTimer < 0.1:    
                self.Explote(12)
            else:                
                self.inDangerTimer = self.inDangerTimer - (self.speed/10)
    
    def InDangerZoneReset(self):
        self.Reset()
        self.state = 1
        
    def GetState(self):
        return self.state
        
            





