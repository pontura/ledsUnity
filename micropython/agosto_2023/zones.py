import zone, utils

class Zones:
    color = 0
    all = []    
    global leds
    
    def Init(self, _color : int, leds) :
        self.leds = leds
        self.color = _color
        self.all = []
            
    def Add(self, ledID : int, width : int) :    
        z = zone.Zone()
        z.Init(ledID, width)
        self.all.append(z)
                
    def Update(self, deltaTime):        
        lN = len(self.all)      
        for a in range(lN):        
            p = self.all[a]
            p.Move(deltaTime)
            for a in range(p.w):
                pos = utils.GetPos(p.ledID+a)
                self.leds.AddAlpha(self.color, pos, 0.1)
    
    def CheckCollisionIn(self, ledID : int):
        lN = len(self.all)      
        for a in range(lN):        
            p = self.all[a]
            for a in range(p.w):   
                if utils.GetPos(p.ledID+a) == ledID:
                    return True
                
        return False
             



