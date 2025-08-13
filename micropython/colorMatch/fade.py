import time
import random

class Fade:
    
    global game
    numpix = 300
    ledID = 0
    gotoNext = 0

    def Init(self, game, numpix):
        self.numpix = numpix
        self.game = game
            
    def InitFade(self, gotoNext):
        self.gotoNext = gotoNext
        
    def OnUpdate(self):
        self.game.SetLed(self.ledID, 0 )
        self.ledID = self.ledID + 1
        if self.ledID>=numpix/2:
            self.ledID = 0
            self.game.GotoState(self.gotoNext)
        else:
            self.game.SetLed(self.ledID, 10 )



