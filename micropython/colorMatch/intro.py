import time
import random

class Intro:
    
    global game
    numpix = 300
    max_colors = 6

    max_len=20
    min_len = 5
    #pixelnum, posn in flash, flash_len, direction
    flashing = []

    num_flashes = 10
    
    timer = 0

    
        

    def Init(self, game, numpix):
        self.numpix = numpix
        self.game = game
        for i in range(self.num_flashes):
            self.pix = random.randint(0, numpix - 1)
            flash_len = random.randint(self.min_len, self.max_len)
            self.flashing.append([self.pix, random.randint(1, self.max_colors), flash_len, 0, 1])
        
    def OnUpdate(self):
        self.timer = self.timer + 1
        if self.timer>2:
            self.timer = 0
            self.game.Fade(4)
        else:
            for i in range(self.num_flashes):

                pix = self.flashing[i][0]
                brightness = (self.flashing[i][3]/self.flashing[i][2])
                self.game.SetLedAlpha(pix, self.flashing[i][1],brightness )

                if self.flashing[i][2] == self.flashing[i][3]:
                    self.flashing[i][4] = -1
                if self.flashing[i][3] == 0 and self.flashing[i][4] == -1:
                    pix = random.randint(0, self.numpix - 1)
                    col = random.randint(1, self.max_colors)
                    flash_len = random.randint(self.min_len, self.max_len)
                    self.flashing[i] = [pix, col, flash_len, 0, 1]
                self.flashing[i][3] = self.flashing[i][3] + self.flashing[i][4]
                time.sleep(0.005)

