import urandom

class Character:
    global game
    width = 0
    characterID = 0
    ledId = 0
    color = 0
    color2 = 0
    
    def Init(self, game, characterID, ledID, width, totalColors):
        self.game = game
        self.width = width
        self.characterID = characterID
        self.ledId = ledID
        
    def Restart(self):
        self.state = 1  
        self.color2 = urandom.randint(1, self.game.totalColors)
        self.ChangeColors()

    def ChangeColors(self):
        c = self.color2
        self.color = c
        self.color2 = c+1
        
        if self.color2 > self.game.totalColors:
            self.color2 = 1

    #def Draw(self, numLeds):
        #if self.characterID == 1:
            #c1 = numLeds - 2
            #c2 = numLeds   -1       
       # else:
           # c2= 0
           # c1= 1
        self.game.SetCharacterColor(self.characterID, self.color)
        #self.game.SetLed(c1, self.color)
        #self.game.SetLed(c2, self.color2)
        
    def Hide(self, numLeds):
        if self.characterID == 1:
            c1 = numLeds - 2
            c2 = numLeds   -1       
        else:
            c2= 0
            c1= 1
        self.game.SetCharacterColor(self.characterID, 0)
        #self.game.SetLed(c1, 0)
        #self.game.SetLed(c2, 0)
