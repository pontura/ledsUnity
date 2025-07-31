import machine
import neopixel
import time
import random

class LightSignals:
    
    id_1 = 0
    id_2 = 0
    color_1 = (0,0,0)
    color_2 = (0,0,0)
    
    def __init__(self, pin_num=1, num_pixels=18):
        self.num_pixels = num_pixels
        self.pin = machine.Pin(pin_num)
        self.strip = neopixel.NeoPixel(self.pin, self.num_pixels)
        self.strip.write()
            
    def SetCharacter1(self, color):
        self.color1 = color
        self.id_1 = 9
        
    def SetCharacter2(self, color):
        self.color2 = color 
        self.id_2 = 9 

    def OnUpdate(self):
        if self.id_1>0:
            self.strip[9-self.id_1] = self.color1
            self.strip.write()
            self.id_1 = self.id_1-1
        if self.id_2>0:
            self.strip[18-self.id_2] = self.color2
            self.strip.write()
            self.id_2 = self.id_2-1
        
