import urandom

class Character:
    global game
    width = 0
    wa = 0
    characterID = 0
    ledId = 0
    totalColors = 0
    color = 0
    color2 = 0
    
    def Init(self, game, characterID, ledID, width, totalColors):
        self.game = game
        self.width = width
        self.characterID = characterID
        self.ledId = ledID
        self.Restart()
        
    def Restart(self):
        self.wa = 1
        self.totalColors = self.game.totalColors
        self.state = 1  
        self.color = urandom.randint(0, self.totalColors - 1)
        self.color2 = self.color
        self.ChangeColors()

    def ChangeColors(self):
        self.wa = 1
        self.color = self.color2
        self.SetSecondaryColor()

    def SetSecondaryColor(self):
        self.color2 = urandom.randint(0, self.game.totalColors - 1)  
        if self.color2 == self.color:
            self.SetSecondaryColor()            

    def Draw(self, numLeds):
        
        if self.wa < self.width:
            self.wa = self.wa+1
            
        w = self.wa/2
        if self.characterID == 1:
            f = numLeds - 1 - self.wa
            t = numLeds
            for a in range( f, t):
                if a >= numLeds - 2:
                    self.game.ledsData[a] = self.game.colors[self.color2]
                else:
                    self.game.ledsData[a] = self.game.colors[self.color]
        else:
            f = 0
            t = self.wa
            for a in range(f, t):
                if a > 2:
                    self.game.ledsData[a] = self.game.colors[self.color]
                else:
                    self.game.ledsData[a] = self.game.colors[self.color2]  