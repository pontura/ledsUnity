import machine
import neopixel
import time
import random

class LightSignals:
    
    ledsSize = 9
    id_1 = 0
    id_2 = 0
    color_1 = (0,0,0)
    color_2 = (0,0,0)
    
    def __init__(self, pin_num=1):
        self.num_pixels = ledsSize*2
        self.pin = machine.Pin(pin_num)
        self.strip = neopixel.NeoPixel(self.pin, self.num_pixels)
        self.strip.write()
            
    def SetCharacter1(self, color):
        self.color1 = color
        self.id_1 = ledsSize
        
    def SetCharacter2(self, color):
        self.color2 = color 
        self.id_2 = ledsSize 

    def OnUpdate(self):
        if self.id_1>0:
            self.strip[ledsSize-self.id_1] = self.color1
            self.strip.write()
            self.id_1 = self.id_1-1
        if self.id_2>0:
            self.strip[ledsSize-1+self.id_2] = self.color2
            self.strip.write()
            self.id_2 = self.id_2-1
        
