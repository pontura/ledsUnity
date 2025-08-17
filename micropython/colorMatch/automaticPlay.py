import time
import random

class AutomaticPlay:
    
    global game
    p1 = 0
    p2 = 2
    delay1 = 0
    delay2 = 0
    rand_from = 30
    rand_to = 120
    timer = 0
    timerToIntro = 1000

    def Init(self, game):
        self.game = game
        self.delay1 = random.uniform(self.rand_from, self.rand_to)
        self.delay2 = random.uniform(self.rand_from, self.rand_to)
            
    def Restart(self):
        self.timer = 0
        self.ledID = 0
        
    def OnUpdate(self):
        if self.timer > self.timerToIntro:
            self.Restart()
            self.game.Fade(1, 2)
        else:
            self.timer = self.timer + 1
            if(self.p1 > self.delay1):
                self.Do(1)
                self.delay1 = random.uniform(self.rand_from, self.rand_to)
                self.p1 = 0
            else:
                self.p1 = self.p1 +1
                
            if(self.p2 > self.delay2):
                self.Do(2)
                self.delay2 = random.uniform(self.rand_from, self.rand_to)
                self.p2 = 0
            else:
                self.p2 = self.p2 +1
            
    def Do(self, p):
        r = random.uniform(0, 10)
        if r > 3 and self.game.Match(p):
            self.Shoot(p)
        else:
            self.Change(p)
            
    def Shoot(self, p):
        print(p)
        self.game.DoShoot(p)
        
    def Change(self, p):
        self.game.DoChangeColors(p, False)
