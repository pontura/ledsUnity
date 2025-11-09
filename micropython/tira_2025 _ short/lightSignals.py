import machine
import neopixel
import time
import random

class LightSignals:
    
    id_1 = 0
    id_2 = 0
    color_1 = (0,0,0)
    color_2 = (0,0,0)
    winColor = (100,100,100)
    loseColor = (255,0,0)
    offColor = (0,0,0)
    max_late = 200
    lateOn = False
    boolLate = False
    lateID = 0.0
    lateSpeed = 0.75
    
    def __init__(self, pin_num=14, num_pixels=23):
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
            
    def Late(self):
        for i in range(9, 14):
        
            if self.lateOn == False:
                if self.boolLate == True:
                    self.boolLate = False
                    self.lateID += self.lateSpeed
                    if self.lateID>=self.max_late:
                        self.lateOn = True
                        self.lateID = self.max_late
                else:
                    self.boolLate = True
                    
            else:
                if self.boolLate == True:
                    self.boolLate = False
                    self.lateID -= self.lateSpeed
                    if self.lateID<=5:
                        self.lateOn = False
                        self.lateID = 5
                    
                else:
                    self.boolLate = True
                    
            v = int(self.lateID)
            self.strip[i] = (v,v,v)
            self.strip.write()

    def UpdateGame(self):
    
        if self.id_1>0:
            self.strip[self.id_1-1] = self.color1
            self.strip.write()
            self.id_1 = self.id_1-1
        if self.id_2>0:
            self.strip[13+self.id_2] = self.color2
            self.strip.write()
            self.id_2 = self.id_2-1
            
            
    def White(self):
        
        for i in range(0, 9):
            self.strip[i] = self.winColor
        for i in range(14, 23):
            self.strip[i] = self.winColor
                
        self.strip.write()
            
            
    def Win(self, ch):
        
        for i in range(0, 9):
            if ch==2:
                self.strip[i] = self.winColor
            else:
                self.strip[i] = self.loseColor
        for i in range(14, 23):
            if ch==2:
                self.strip[i] = self.loseColor
            else:
                self.strip[i] = self.winColor
                
        self.strip.write()
        
    def Off(self):
        
        for i in range(0, 9):
            self.strip[i] = self.offColor
        for i in range(14, 23):
            self.strip[i] = self.offColor
                
        self.strip.write()
        
