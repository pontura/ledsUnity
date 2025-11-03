import time
import random

class Fade:
    
    global game
    numpix = 300
    ledID = 0
    gotoNext = 0
    color = 10

    def Init(self, game, numpix):
        self.numpix = numpix
        self.game = game
            
    def InitFade(self, gotoNext, color):
        self.gotoNext = gotoNext
        self.color = color
        
    def OnUpdate(self):
        self.game.SetLed(self.ledID, 0 )
        led2 = self.numpix-self.ledID-1        
        self.game.SetLed(led2, 0 )
        
        self.ledID = self.ledID + 1
        led2 = self.numpix-self.ledID-1  
        if self.ledID>=self.numpix/2:
            self.ledID = 0
            self.game.GotoState(self.gotoNext)
        else:
            self.game.SetLed(self.ledID, self.color )
            self.game.SetLed(led2, self.color )



