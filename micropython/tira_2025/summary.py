import urandom
import time

class Summary:
    global game
    num_leds = 300
    led_ids = []
    note_duration = 2
    note_duration_end = 1
    fade_time = 1.0
    fade_steps = 50
    target_alpha = 155
    color = (255, 255, 255)
    timer = 0
    v = 0.05
    ledID = 0
    noiseLedID = 0
    playerID = 0
    done = False
    
    def Init(self, game, num_leds):
        self.game = game
        self.num_leds = num_leds

    def play_victory(self, playerID):
        self.playerID = playerID
        if playerID ==2:
            self.led_ids = range(0, int(self.num_leds/2))
        else:
            self.led_ids = range(int(self.num_leds/2), self.num_leds)
            
        self.led_ids = self.shuffle_array( self.led_ids)
        
        self.note = 0
        self.timer = 0
        self.v = 0.05
        self.ledID = 0
        self.noiseLedID = 0
        self.done = False
        
    def shuffle_array(self, arr):
        arr = list(arr)  # 🔹 convierte a lista si era un range o tupla
        for i in range(len(arr) - 1, 0, -1):
            j = urandom.getrandbits(16) % (i + 1)
            arr[i], arr[j] = arr[j], arr[i]
        return arr
    
            
    def OnUpdate(self, deltaTime):
        
        self.ledID = self.ledID +1
        if self.ledID<int(self.num_leds/2)-1:
            if self.done == True:                
                self.game.SetLedAlpha(self.led_ids[self.ledID], 0, 0.1)
            else:                    
                self.game.SetLedAlpha(self.led_ids[self.ledID], 10, 0.1) 
            
        else:
            if self.done == True:
                for led_id in self.led_ids:
                    self.game.SetLedAlpha(led_id, 0, 0)
                self.End()
            else:
                for led_id in self.led_ids:
                    
                    self.v = 1
                    self.done = True
                    self.ledID = 0
                    self.game.SetLedAlpha(led_id, 10, 0.5)
            
        self.timer = self.timer + deltaTime
        if self.note>2:
            self.v = self.v - 0.01
        else:
            if urandom.randint(1, 10)>3:
                self.v = self.v + 0.01
            else:
                self.v = self.v - 0.02
            if self.timer > self.note_duration:
                self.PlayNote()
                
        self.game.LoopNote(self.v, 1)
            
        

            
    def PlayNote(self):
        self.note = self.note +1
        self.timer = 0
        
        
    def End(self):            
        self.game.GotoState(1)

