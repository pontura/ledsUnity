import time
import random

class AutomaticPlay:
    
    global game
    p1 = 0
    p2 = 2
    delay1 = 0
    delay2 = 0

    def Init(self, game):
        self.game = game
        self.delay1 = random.uniform(0.8, 2)
        self.delay2 = random.uniform(0.8, 2)
            
    def Restart(self):
        self.ledID = 0
        
    def OnUpdate(self):
        if(self.p1 > self.delay1):
            self.Do(1)
            self.delay1 = random.uniform(0.5, 2)
            self.p1 = 0
        else:
            self.p1 = self.p1 +1
            
        if(self.p2 > self.delay2):
            self.Do(2)
            self.delay2 = random.uniform(0.5, 2)
            self.p2 = 0
        else:
            self.p2 = self.p2 +1
            
    def Do(self, p):
        r = random.uniform(0, 10)
        if r > 5:
            Shoot(p)
        else:
            Change(p)
            
    def Shoot(self, p):
        pint(p)
        self.game.Shoot(p)
        
     def Change(self, p):
        self.game.ChangeColors(p, false)
