from machine import Pin, PWM
from utime import sleep
import audioSource

class Audio:    
    a = []
    
    def Init(self):        
        a1 = audioSource.AudioSource()
        a2 = audioSource.AudioSource()
        
        a1.SetPin(self, 0, 1)
        a2.SetPin(self, 1, 2)

        self.a.append(a1)
        self.a.append(a2)   
    
    def LoopNote(self, note, ch:int):
        self.a[ch-1].SetNote(note)       
        self.Play(6, 0.04, ch)
        
    
    def Tick(self, ch : int):
        if self.a[ch-1].clip == 0:
            self.Play(1, 0.06, ch)
            
    def Fire(self, ch : int):
        self.Play(2, 0.4, ch)
        
    def Swap(self, ch : int, color : int):
        self.Play(3, 0.1, ch)
        
    def Explote(self, ch : int):
        self.Play(4, 0.3, ch)
        
    def Wrong(self, ch : int):
        self.Play(5, 0.2, ch)
    
    def Play(self, clip:int, dur:float, ch: int):
        self.a[ch-1].Play(clip, dur)       
        
            
    def OnUpdate(self, deltaTime):        
            self.a[0].OnUpdate(deltaTime)
            self.a[1].OnUpdate(deltaTime)
    
    def Stop(self, ch : int):
        self.a[ch-1].be_quiet()
            
