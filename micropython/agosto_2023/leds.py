from machine import Pin
import rp2
import array

class Leds:
    
    PIN_NUM = 22
    NUM_LEDS = 300

    @rp2.asm_pio(sideset_init=rp2.PIO.OUT_LOW, out_shiftdir=rp2.PIO.SHIFT_LEFT, autopull=True, pull_thresh=24)
    def ws2812():
        T1 = 2
        T2 = 5
        T3 = 3
        wrap_target()
        label("bitloop")
        out(x, 1)               .side(0)    [T3 - 1]
        jmp(not_x, "do_zero")   .side(1)    [T1 - 1]
        jmp("bitloop")          .side(1)    [T2 - 1]
        label("do_zero")
        nop()                   .side(0)    [T2 - 1]
        wrap()

    sm = rp2.StateMachine(0, ws2812, freq=8_000_000, sideset_base=Pin(PIN_NUM))
    sm.active(1)
    
    dimmer_ar = []
    empty = []
    bgColor = 0
    red = 0
    green = 0
    blue = 0
    yellow = 0
    white = 0
    
    def Init(self):
        self.dimmer_ar = array.array("I", [0 for _ in range(self.NUM_LEDS)])
        self.bgColor = self.CreateColor((0,0,0))
        self.red = self.CreateColor(self.RED)
        self.green = self.CreateColor(self.GREEN)
        self.blue = self.CreateColor(self.BLUE)
        self.white = self.CreateColor(self.WHITE)
        self.yellow = self.CreateColor(self.YELLOW)
         
    def Update(self):
        for a in range(self.NUM_LEDS):
            self.dimmer_ar[a] = self.bgColor
            
    @micropython.viper      
    def Add(self, colorName : int, id : int):
        c = ""
        if colorName == 1:
            c = self.red
        elif colorName == 2:
            c = self.green
        elif colorName == 3:
            c = self.blue
        elif colorName == 0:
            c = self.white
        elif colorName == 4:
            c = self.yellow
        self.dimmer_ar[id] = c
        
        
    def AddAlpha(self, colorName : int, id : int, alpha : float):
        c = ""
        if colorName == 1:
            c = self.red
        elif colorName == 2:
            c = self.green
        elif colorName == 3:
            c = self.blue
        elif colorName == 0:
            c = self.yellow
            
        self.SetPixelBrighteness(c, id, alpha)
    
    def GetColor(self, colorName) -> int:
        if colorName == "red":
            return 1
        elif colorName == "green":
            return 2
        elif colorName == "blue":
            return 3
        else:
            return 0
        
    @micropython.viper 
    def SetLeds(self):  
        self.sm.put(self.dimmer_ar, 8)
        
    def CreateColor(self, color):
        c = self.setColor(color)
        r = int(((c >> 8) & 0xFF) )
        g = int(((c >> 16) & 0xFF))
        b = int((c & 0xFF) )
        return (g<<16) + (r<<8) + b
        
    def SetPixelBrighteness(self, color, id : int, brightness : float):
        c = color
        r = int(((c >> 8) & 0xFF) * brightness )
        g = int(((c >> 16) & 0xFF) * brightness)
        b = int((c & 0xFF) * brightness)
        self.dimmer_ar[id] = (g<<16) + (r<<8) + b    
       

    
    BLACK = (0, 0, 0)
    RED = (255, 0, 0)
    BLUE = (0, 0, 255)
    YELLOW = (255, 150, 0)
    GREEN = (0, 255, 0)
    WHITE = (255, 255, 255)

    def setColor(self, color):
        return (color[1]<<16) + (color[0]<<8) + color[2]







