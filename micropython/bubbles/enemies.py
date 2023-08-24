import urandom

class Enemies:
    global game
    state = 0
    
    #state = 1 on destroy player 1
    #state = 2 on destroy player 2
    
    #state = 3 dead
    
    damage = 0
    chararter_width = 0
    
    def __init__(self):
        self.data = []
        self.data2 = []
        self.numLeds = 0
        self.bubbleTotalWidth = 8
        self.bbw_ch1 = 0
        self.bbw_ch2 = 0
        self.currentColor = 0
        self.currentColor2 = 0
        self.game = None
        self.centerLedID = 0

    def Init(self, game, chararter_width, numLeds, _c):        
        self.colors = _c
        self.chararter_width = chararter_width
        self.game = game
        self.data = []
        self.data2 = []
        self.Restart()
        self.numLeds = numLeds

    def Restart(self):
        self.state = 0
        self.data.clear()
        self.data2.clear()

    def UpdateDraw(self, ch, centerLedID):
        self.centerLedID = centerLedID
        
        if ch == 1:
            if self.bbw_ch1 >= self.bubbleTotalWidth:
                self.set_new_bubble1()
                self.bbw_ch1 = 0            
            else:
                self.bbw_ch1 += 1
        else:
            if self.bbw_ch2 >= self.bubbleTotalWidth:
                self.set_new_bubble2()
                self.bbw_ch2 = 0
            else:
                self.bbw_ch2 += 1

        self.destroy_line(ch)
        self.add_line(ch)
        self.add_line(ch)
        self.Draw(centerLedID)

    def CleanLeds(self, centerLedID: int, from_: int, to: int, ch:int , c:int):
        self.centerLedID = centerLedID
        c = 0
      #  c = 1+0.01
    #         c1 = self.colors[c1] + 0.1
    #         c2 = self.colors[c2] + 0.1
        if ch == 1:
            firstMid = centerLedID - len(self.data2)
#             self.game.strip.set_pixel_line(from_, firstMid, (0,0,0))
            for a in range(from_, firstMid):
                self.game.SetLed(a, c)
        else:
            lastMid = centerLedID + len(self.data)            
#             self.game.strip.set_pixel_line(lastMid, to, (0,0,0))
            for a in range(lastMid, to):
                self.game.SetLed(a, c)

    def Draw(self, centerLedID : int):
        ledId = 0
        c = 0
        for colorID in self.data:
            c = self.colors[colorID]
                
            ledID = ledId + centerLedID
            if ledID > self.numLeds - self.chararter_width:
                self.game.Win(2)
                return
            self.game.SetLed(ledID, c)
#             self.game.ledsData[ledID] = c
            ledId += 1

        ledId = 0
        for colorID in self.data2:            
            c = self.colors[colorID]
                
            ledID = centerLedID - ledId
            if ledID < self.chararter_width:
                self.game.Win(1)
                return
            self.game.SetLed(ledID, c)
#             self.game.ledsData[ledID] = c
            ledId += 1
            
    def AnimHit(self):
        if(self.state==1):
            self.game.centerLedID = self.game.centerLedID - 1
        else:
            self.game.centerLedID = self.game.centerLedID + 1
        self.damage = self.damage -1
        if self.damage <=0:
            self.state = 0
        else:
            self.Draw(self.game.centerLedID)
        
    def destroy_line(self, ch):
        if ch == 1 and len(self.data) > 0:
            self.data.pop()
        elif ch == 2 and len(self.data2) > 0:
            self.data2.pop()

    def add_line(self, ch):
        if ch == 1:
            self.data.insert(0, self.currentColor)
        else:
            self.data2.insert(0, self.currentColor2)

    def CollideWith(self, color, characterID):
        if characterID == 1:
            if len(self.data) > 1 and self.data[-1] == color:
                self.destroy_last_color1(color)
            else:
                self.add_colors(color, characterID)
        else:
            if len(self.data2) > 1 and self.data2[-1] == color:
                self.destroy_last_color2(color)
            else:
                self.add_colors(color, characterID)
        self.Draw(self.centerLedID)

    def destroy_last_color1(self, color):
        from_ = 0
        to = 0
        f = len(self.data) - 1
        for a in range(f, 0, -1):
            if self.data[a] == color:
                self.data.pop()
                if to == 0:
                    to = a + self.centerLedID
            else:
                from_ = self.centerLedID + a
                self.Kill(from_, to, 1, color)
                return                
        if to != 0:
            from_ = self.centerLedID
            self.Kill(from_, to, 1, color)   

    def destroy_last_color2(self, color):
        from_ = 0
        to = 0
        for a in range(len(self.data2) - 1, 0, -1):
            if self.data2[a] == color:
                self.data2.pop()
                if from_ == 0:
                    from_ = self.centerLedID - a
            else:
                to = self.centerLedID - a
                self.Kill(from_, to, 2, color)
                return            
        if from_ != 0:
            to = self.centerLedID
            self.Kill(from_, to, 2, color)
            
    def Kill(self, _from, _to, characterID, color):
        self.damage = int((_to-_from)/1.1)
        if self.damage<2:
            self.damage = 2
        self.game.AddExplotion(_from, _to, characterID, color)
        self.game.OnReward(characterID, self.damage)
        self.state = characterID

    def add_colors(self, color, characterID):
        self.game.Wrong()
        for _ in range(self.bubbleTotalWidth):
            if characterID == 1:
                self.data.append(color)
            else:
                self.data2.append(color)
                
        self.Draw(self.centerLedID)

    def set_new_bubble1(self):
        newColor = urandom.randint(0, self.game.totalColors - 1)
        if newColor == self.currentColor:
            self.set_new_bubble1()
        else:
            self.currentColor = newColor

    def set_new_bubble2(self):
        newColor = urandom.randint(0, self.game.totalColors - 1)
        if newColor == self.currentColor2:
            self.set_new_bubble2()
        else:
            self.currentColor2 = newColor
    
    
    def GameOver(self, ch):
        self.state = 3
        
    deadTimer = 0
    def AnimDead(self, deltaTime, centerLedID, ch, animated: bool):
        if(animated == True):
            if ch == 1:           
                if len(self.data2)> 0:
                    self.data2.pop()
                elif len(self.data)> 0:
                    self.data.pop()
                else:
                    self.game.Restart()
                    return                
            elif ch == 2:         
                if len(self.data)> 0:
                    self.data.pop()
                elif len(self.data2)> 0:
                    self.data2.pop()
                else:
                    self.game.Restart()
                    return
            
        self.deadTimer += deltaTime
        if(self.deadTimer<0.1):            
            self.PlayLoopDeath(True)
            ledId = 0            
            for colorID in self.data:
                c = self.colors[colorID]                
                ledID = ledId + centerLedID          
                self.SetLed(ledID,c+0.1)
                ledId += 1

            ledId = 0
            for colorID in self.data2:            
                c = self.colors[colorID]                
                ledID = centerLedID - ledId
                self.SetLed(ledID,c+0.1)
                ledId += 1
                
        elif(self.deadTimer<0.2):
                  
            self.PlayLoopDeath(False)
            ledId = 0            
            for colorID in self.data:
                c = self.colors[colorID]                
                ledID = ledId + centerLedID
                self.SetLed(ledID,c)
                ledId += 1

            ledId = 0
            for colorID in self.data2:            
                c = self.colors[colorID]                
                ledID = centerLedID - ledId
                self.SetLed(ledID,c)
                ledId += 1
                
        else:
            self.deadTimer = 0
            
    def SetLed(self, ledID, c):
        if ledID<0:
            return
        elif ledID>self.numLeds:
            return
        self.SetLed(ledID,c)
#         self.game.ledsData[ledID] = c
        
    def PlayLoopDeath(self, on : bool):
        v = 0
        if on:
            v =  (len(self.data2) + len(self.data)) / self.numLeds
        else:
            v = 0
        self.game.LoopNote(v)
            
        
