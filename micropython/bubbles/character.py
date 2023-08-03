import urandom

class Character:
    global game
    width = 0
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
        self.state = 1
        self.totalColors = totalColors
        self.color = urandom.randint(1, totalColors - 1)
        self.color2 = self.color
        self.ChangeColors()

    def ChangeColors(self):
        self.color = self.color2
        self.SetSecondaryColor()

    def SetSecondaryColor(self):
        self.color2 = urandom.randint(1, self.game.totalColors - 1)       
        
        if self.color2 == self.color:
            self.SetSecondaryColor()

    def Draw(self, numLeds):
        if self.characterID == 1:
            for a in range( numLeds - 1 -self.width, numLeds):
                if a >= numLeds - 1 - self.width/2:
                    self.game.ledsData[a] = self.game.colors[self.color2]
                else:
                    self.game.ledsData[a] = self.game.colors[self.color]
        else:
             for a in range(0, self.width):
                if a >= self.width /2:
                    self.game.ledsData[a] = self.game.colors[self.color]
                else:
                    self.game.ledsData[a] = self.game.colors[self.color2]  