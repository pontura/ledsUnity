from machine import Pin, PWM
import random

class AudioSource:
    ch = 0
    clip = 0    
    dur = 0
    timer = 0
    note = 0
    
    global buzzer
    start_value = 400
    clipState = 0
    pint = 0
    
    def SetPin(self, audio, pin, ch):
        self.ch = ch
        self.audio = audio
        self.pin = pin
        self.buzzer = PWM(Pin(pin))
    
    def SetNote(self, note):
        self.note = note
        
    def Play(self, clip, dur):
        self.timer = 0
        self.clip = clip
        self.dur = dur
        if clip  == 1:
            self.Tick_init()
        elif clip == 2:
            self.Fire_init()
        elif clip == 3:
            self.Swap_init()
        elif clip == 4:
            self.Explote_init()
        elif clip == 5:
            self.Wrong_init()
        
    def OnUpdate(self, deltaTime):
        self.timer = self.timer + deltaTime
        if self.timer > self.dur:
            self.Stop()
        elif self.clip  == 1:
            self.Tick()
        elif self.clip == 2:
            self.Fire()
        elif self.clip == 3:
            self.Swap()
        elif self.clip == 4:
            self.Explote()
        elif self.clip == 5:
            self.Wrong()
        elif self.clip == 6:
            self.LoopNote(self.note)
        
    def Stop(self):
        self.timer = 0
        self.clip = 0
        self.dur = 0
        self.audio.Stop(self.ch)
    
   
        
    
    def LoopNote(self, note:float):
        f = 500 + (note*5000)
        self.play_tone(f, 0.95)
        
    def Tick_init(self):
        self.start_value = 300        
    def Tick(self):      
        v = self.start_value - (self.timer*500)
        if v>0:
            self.play_tone(v, 0.01)
            
            
            
    def Fire_init(self):
        self.start_value = 2000
        self.clipState  =0
        
    def Fire(self):
        v = 1
        f = 5000
        if self.timer < 0.06:
            f = self.start_value - (self.timer*2400)
        elif self.clipState == 0:
            self.start_value = 1000
            self.clipState = 1
            v = 0.7
        else:            
            f = self.start_value - (self.timer*1000)
            v = 0.7-(self.timer*1.7)            
        if f<100:
            f = 100
        elif f>60000:
            f = 60000
        if v >0:
            self.play_tone(f, v)
            
            
    def Swap_init(self):
        self.start_value = 1000
        self.clipState  =0
    def Swap(self):
        v = 1
        f = 5000
        if self.timer < 0.02:
            f = self.start_value - (self.timer*2400)
        elif self.clipState == 0:
            self.start_value = 500
            self.clipState = 1
            v = 0.7
        else:            
            f = self.start_value + (self.timer*1000)
            v = 0.7-(self.timer*1.7)            
        if f<100:
            f = 100
        elif f>60000:
            f = 60000
        if v >0:
            self.play_tone(f, v)
            
            
    def Explote_init(self):
        self.clipState  =0
    def Explote(self):
        f = random.randint(150,1450)  
        v = 1-(self.timer*1.5)
        if v >0:
            self.play_tone(f, v)
            
            
    def Wrong_init(self):
        self.clipState  =0
    def Wrong(self):
        f = random.randint(150,250)  
        v = 1-(self.timer*1.7)
        if v >0:
            self.play_tone(f, v)
            
    
    def play_tone(self, frequency, volume : float):
        if frequency<100:
            frequency = 100
        self.buzzer.duty_u16(int(volume*65536))
        self.buzzer.freq(int(frequency))

    def be_quiet(self):
        self.buzzer.duty_u16(0)