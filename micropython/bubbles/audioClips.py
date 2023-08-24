from machine import Pin, PWM
from utime import sleep
import random

class Clips:
    
    buzzer = PWM(Pin(2))
    timer = 0
    start_value = 400
    clipState = 0
    
    def LoopNote(self, note:float):
        f = 500 + (note*5000)
        self.play_tone(f, 0.95)
        
    def Tick_init(self):
        self.start_value = 300        
    def Tick(self, timer):      
        v = self.start_value - (timer*500)
        if v>0:
            self.play_tone(v, 0.01)
            
            
            
    def Fire_init(self):
        self.start_value = 2000
        self.clipState  =0
    def Fire(self, timer):
        v = 1
        f = 5000
        if timer < 0.06:
            f = self.start_value - (timer*2400)
        elif self.clipState == 0:
            self.start_value = 1000
            self.clipState = 1
            v = 0.7
        else:            
            f = self.start_value - (timer*1000)
            v = 0.7-(timer*1.7)            
        if f<100:
            f = 100
        elif f>60000:
            f = 60000
        if v >0:
            self.play_tone(f, v)
            
            
    def Swap_init(self):
        self.start_value = 1000
        self.clipState  =0
    def Swap(self, timer):
        v = 1
        f = 5000
        if timer < 0.02:
            f = self.start_value - (timer*2400)
        elif self.clipState == 0:
            self.start_value = 500
            self.clipState = 1
            v = 0.7
        else:            
            f = self.start_value + (timer*1000)
            v = 0.7-(timer*1.7)            
        if f<100:
            f = 100
        elif f>60000:
            f = 60000
        if v >0:
            self.play_tone(f, v)
            
            
    def Explote_init(self):
        self.clipState  =0
    def Explote(self, timer):
        f = random.randint(150,1450)  
        v = 1-(timer*1.5)
        if v >0:
            self.play_tone(f, v)
            
            
    def Wrong_init(self):
        self.clipState  =0
    def Wrong(self, timer):
        f = random.randint(150,250)  
        v = 1-(timer*1.7)
        if v >0:
            self.play_tone(f, v)
            
    
    def play_tone(self, frequency, volume : float):
        if frequency<100:
            frequency = 100
        self.buzzer.duty_u16(int(volume*65536))
        self.buzzer.freq(int(frequency))

    def be_quiet(self):
        self.buzzer.duty_u16(0)