import time
import random

class GameInit:
    
    global game
    numpix = 300
    ledID = 0

    def Init(self, game, numpix):
        self.numpix = numpix
        self.game = game
        for l in range(self.numpix):
            self.game.SetLed(l, 0)
            
    def Restart(self):
        self.ledID = 0
        
    def OnUpdate(self):        
        #RESET
        l1 = self.ledID
        self.game.SetLed(l1, 0)
        l2 = self.numpix-self.ledID-1
        self.game.SetLed(l2, 0)
        
        self.ledID = self.ledID +1
        if self.ledID >=self.numpix/2:
            self.Restart()
            self.game.GotoState(2)
        else:        
            l1 = self.ledID
            self.game.SetLed(l1, 10)
            l2 = self.numpix-self.ledID-1
            self.game.SetLed(l2, 10)

