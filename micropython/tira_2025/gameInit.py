import time
import random

class GameInit:
    
    global game
    numpix = 300
    ledID = 0
    speed = 0.5
    v = 0.05

    def Init(self, game, numpix):
        self.numpix = numpix
        self.game = game        
            
    def Restart(self):
        for l in range(self.numpix):
            self.game.SetLedAlpha(l, 10, 0.1)
        self.ledID = 0
        self.v = 0.05
        
    def OnUpdate(self):        
        #RESET
        l1 = int(self.ledID)
        self.game.SetLed(l1, 0)
        l2 = self.numpix-int(self.ledID)-1
        self.game.SetLed(l2, 0)
        
        self.ledID = self.ledID +self.speed
        led = int(self.ledID +self.speed)
        if led >=self.numpix/2:
            self.game.GotoState(2)
        else:        
            l1 = led
            self.game.SetLed(l1, 10)
            l2 = self.numpix-led-1
            self.game.SetLed(l2, 10)
            self.v = self.v + 0.005
            self.game.LoopNote(self.v, 1)

