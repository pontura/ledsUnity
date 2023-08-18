from machine import Pin, PWM
from utime import sleep
import audioClips

class Audio:
    
    a = audioClips.Clips()
    clip = 0
    dur = 0
    timer = 0
    note = 0
    
    def LoopNote(self, _note):
        self.note = _note
        self.Play(6, 0.04)
    
    def Tick(self):
        if self.clip == 0:
            self.Play(1, 0.06)
            
    def Fire(self):
        self.Play(2, 0.4)
        
    def Swap(self):
        self.Play(3, 0.1)
        
    def Explote(self):
        self.Play(4, 0.3)
        
    def Wrong(self):
        self.Play(5, 0.2)
    
    def Play(self, clip:int, dur:float):
        self.clip = clip
        self.dur = dur
        self.timer = 0
        if self.clip  == 1:
            self.a.Tick_init()
        elif self.clip == 2:
            self.a.Fire_init()
        elif self.clip == 3:
            self.a.Swap_init()
        elif self.clip == 4:
            self.a.Explote_init()
        elif self.clip == 5:
            self.a.Wrong_init()
            
    def OnUpdate(self, deltaTime):
        if self.clip == 0:
            return
        self.timer = self.timer + deltaTime
        if self.timer > self.dur:
            self.Stop()
        if self.clip  == 1:
            self.a.Tick(self.timer)
        elif self.clip == 2:
            self.a.Fire(self.timer)
        elif self.clip == 3:
            self.a.Swap(self.timer)
        elif self.clip == 4:
            self.a.Explote(self.timer)
        elif self.clip == 5:
            self.a.Wrong(self.timer)
        elif self.clip == 6:
            self.a.LoopNote(self.note)
    
    def Stop(self):
        self.clip = 0
        self.duration = 0
        self.a.be_quiet()
            
