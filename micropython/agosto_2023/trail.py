import TrailParticle, utils


class Trail:
    color = 2
    all = []
    lastLedID = 0
    trailSpeed = 30
    global leds
    def Init(self, _color : int,  _totalParticles : int, leds) :
        self.leds = leds
        self.color = _color
        self.all = []
        
        for a in range(_totalParticles):   
            particle = TrailParticle.TrailParticle()
            self.all.append(particle)
                
    def Move(self, ledID, _speed, deltaTime):        
        lN = len(self.all)      
        for a in range(lN):        
            p = self.all[a]
            if p.IsAvailable() == False:
                p.OnUpdate(deltaTime*self.trailSpeed)
                
                self.leds.AddAlpha(self.color, p.ledID, p.value)
        if _speed<0:
            ledID = ledID+1
        else:
            ledID = ledID-1
        
        if ledID != self.lastLedID:
            self.lastLedID = ledID 
            for a in range(lN):        
                p = self.all[a]
                if p.IsAvailable():
                    p.Init(ledID)
                    return


