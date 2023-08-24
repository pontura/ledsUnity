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
    
    BLACK = (0, 0, 0)
    WHITE = (255, 255, 255)

    RED = (255, 0, 0)
    GREEN = (0, 255, 0)
    BLUE = (0, 0, 255)

    YELLOW = (255, 255, 0)
    CYAN = (0, 255, 255)
    MAGENTA = (255, 0, 255)
    
    black = 0
    white = 0
    red = 0
    green = 0
    blue = 0
    yellow = 0
    cyan = 0
    magenta = 0
    
    def Init(self):
        self.dimmer_ar = array.array("I", [0 for _ in range(self.NUM_LEDS)])
        self.bgColor = self.CreateColor((0,0,0))
        self.white = self.CreateColor(self.WHITE)
        self.red = self.CreateColor(self.RED)
        self.green = self.CreateColor(self.GREEN)
        self.blue = self.CreateColor(self.BLUE)
        self.yellow = self.CreateColor(self.YELLOW)
        self.cyan = self.CreateColor(self.CYAN)
        self.magenta = self.CreateColor(self.MAGENTA)
        
        for a in range(self.NUM_LEDS):
            self.dimmer_ar[a] = self.bgColor
            
    @micropython.viper 
    def Send(self):  
        self.sm.put(self.dimmer_ar, 8)
      
    @micropython.viper 
    def SetLed(self, colorID : int, id : int):
        self.dimmer_ar[id] = self.GetColor(colorID)
        
    def SetLedAlpha(self, colorID : int, id : int, a : float):
        c = self.GetColor(colorID)                 
        self.SetPixelBrighteness(c, id, a)
        
    @micropython.viper 
    def GetColor(self, colorID : int):
        c = ""
        if colorID == 10:
            c = self.white
        elif colorID == 0:
            c = self.black
        elif colorID == 1:
            c = self.red
        elif colorID == 2:
            c = self.green
        elif colorID == 3:
            c = self.blue
        elif colorID == 4:
            c = self.yellow
        elif colorID == 5:
            c = self.cyan
        elif colorID == 6:
            c = self.magenta
        return c
    
   
        
    def CreateColor(self, color):
        c = self.setColor(color)
        r = int(((c >> 8) & 0xFF) )
        g = int(((c >> 16) & 0xFF))
        b = int((c & 0xFF) )
        return (g<<16) + (r<<8) + b
        
    def SetPixelBrighteness(self, color, id : int, a : float):
        c = color
        r = int(((c >> 8) & 0xFF) * a )
        g = int(((c >> 16) & 0xFF) * a)
        b = int((c & 0xFF) * a)
        self.dimmer_ar[id] = (g<<16) + (r<<8) + b       
  

    def setColor(self, color):
        return (color[1]<<16) + (color[0]<<8) + color[2]







