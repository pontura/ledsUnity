import urandom

class Enemies:
    global game
    def __init__(self):
        self.data = []
        self.data2 = []
        self.numLeds = 0
        self.bubbleTotalWidth = 8
        self.bubbleWidth = 0
        self.currentColor = 0
        self.currentColor2 = 0
        self.game = None
        self.centerLedID = 0

    def Init(self, game, chararter_width, numLeds):
        self.game = game
        self.data = []
        self.data2 = []
        self.Restart()
        self.numLeds = numLeds

    def Restart(self):
        self.data.clear()
        self.data2.clear()

    def UpdateDraw(self, centerLedID):
        self.centerLedID = centerLedID
        if self.bubbleWidth >= self.bubbleTotalWidth:
            self.set_new_bubble1()
            self.set_new_bubble2()
            self.bubbleWidth = 0

        self.destroy_line()
        self.add_line()
        self.add_line()

        self.bubbleWidth += 1
        self.Draw(centerLedID)

    def CleanLeds(self, centerLedID, from_, to):
        self.centerLedID = centerLedID
        firstMid = centerLedID - len(self.data2)
        for a in range(from_, firstMid):
            self.game.ledsData[a] = 0
        lastMid = centerLedID + len(self.data)
        for a in range(lastMid, to):
            self.game.ledsData[a] = 0

    def Draw(self, centerLedID):
        ledId = 0

        for colorID in self.data:
            ledID = ledId + centerLedID
            if ledID > self.numLeds - 5:
                self.game.Win(2)
                return
            self.game.ledsData[ledID] = self.game.colors[colorID]
            ledId += 1

        ledId = 0
        for colorID in self.data2:
            ledID = centerLedID - ledId
            if ledID < 5:
                self.game.Win(1)
                return
            self.game.ledsData[ledID] = self.game.colors[colorID]
            ledId += 1

    def destroy_line(self):
        if len(self.data) > 0:
            self.data.pop()
        if len(self.data2) > 0:
            self.data2.pop()

    def add_line(self):
        self.data.insert(0, self.currentColor)
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

    def destroy_last_color1(self, color):
        from_ = 0
        to = 0
        num = 0
        for a in range(len(self.data) - 1, 0, -1):
            if self.data[a] == color:
                self.data.pop()
                from_ = a + self.centerLedID
                if num == 0:
                    to = a + self.centerLedID
                num += 1
            else:
                if from_ != 0 and to != 0:
                    self.game.AddExplotion(from_, to, 1, color)
                    self.game.OnReward(1, 2)
                return
        self.Draw(self.centerLedID)

    def destroy_last_color2(self, color):
        from_ = 0
        to = 0
        num = 0
        for a in range(len(self.data2) - 1, 0, -1):
            if self.data2[a] == color:
                self.data2.pop()
                to = self.centerLedID - a
                if num == 0:
                    from_ = self.centerLedID - a
                num += 1
            else:
                if from_ != 0 and to != 0:
                    self.game.AddExplotion(from_, to, 2, color)
                    self.game.OnReward(2, 2)
                return
        self.Draw(self.centerLedID)

    def add_colors(self, color, characterID):
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