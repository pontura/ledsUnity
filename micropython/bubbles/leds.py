from machine import Pin
import array
import neopixel

class Leds:   
    
    PIN_NUM = 22
    NUM_PIXELS = 288
    
    np = neopixel.NeoPixel(machine.Pin(PIN_NUM), NUM_PIXELS)
    
    dimmer_ar = []
    
    BLACK = (0, 0, 0)
    WHITE = (255, 255, 255)

    RED = (255, 0, 0)
    GREEN = (0, 255, 0)
    BLUE = (0, 0, 255)

    YELLOW = (255, 255, 0)
    CYAN = (0, 255, 255)
    MAGENTA = (255, 0, 255)
    
    a = 1
    RED2 = (a, 0, 0)
    GREEN2 = (0, a, 0)
    BLUE2 = (0, 0, a)

    YELLOW2 = (a, a, 0)
    CYAN2 = (0, a, a)
    MAGENTA2 = (a, 0, a)
    
    black = 0
    white = 0
    red = 0
    green = 0
    blue = 0
    yellow = 0
    cyan = 0
    magenta = 0
    
    red2 = 0
    green2 = 0
    blue2 = 0
    yellow2 = 0
    cyan2 = 0
    magenta2 = 0
    
    def Init(self, NUM_LEDS):
        self.NUM_LEDS = NUM_LEDS
        self.dimmer_ar = array.array("I", [0 for _ in range(self.NUM_LEDS)])
        
        self.bgColor = self.CreateColor((0,0,0))
        self.white = self.CreateColor(self.WHITE)
        
        self.red = self.CreateColor(self.RED)
        self.green = self.CreateColor(self.GREEN)
        self.blue = self.CreateColor(self.BLUE)
        self.yellow = self.CreateColor(self.YELLOW)
        self.cyan = self.CreateColor(self.CYAN)
        self.magenta = self.CreateColor(self.MAGENTA)
        
        self.red2 = self.CreateColor(self.RED2)
        self.green2 = self.CreateColor(self.GREEN2)
        self.blue2 = self.CreateColor(self.BLUE2)
        self.yellow2 = self.CreateColor(self.YELLOW2)
        self.cyan2 = self.CreateColor(self.CYAN2)
        self.magenta2 = self.CreateColor(self.MAGENTA2)
        
        for a in range(self.NUM_LEDS):
            self.dimmer_ar[a] = self.bgColor
            
#    @micropython.viper 
    def Send(self):
        print("send")
        for i in range(self.NUM_LEDS):
            np[i] = self.dimmer_ar[i]  # Rojo
        np.write()
#         self.sm.put(self.dimmer_ar, 8)
#         s = "".join(str(self.GetStr(n)) for n in self.dimmer_ar)
#         print(s)
         
    def GetStr(self, c):
        if c == self.black:
            return "0"
        elif c == self.white:
            return "9"
        elif c == self.red:
            return "1"
        elif c == self.green:
            return "2"
        elif c == self.blue:
            return "3"
        elif c == self.yellow:
            return "4"
        elif c == self.cyan:
            return "5"
        elif c == self.magenta:
            return "6"
        return "x"
      
   # @micropython.viper 
    def SetLed(self, colorID : int, id : int):
        self.dimmer_ar[id] = self.GetColor(colorID)
    
   # @micropython.viper 
    def SetLed2(self, colorID : int, id : int):
        self.dimmer_ar[id] = self.GetColor2(colorID)
        
    def SetLedAlpha(self, colorID : int, id : int, a : float):
        c = self.GetColor(colorID)                 
        self.SetPixelBrighteness(c, id, a)
        
   # @micropython.viper 
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
    
 #   @micropython.viper 
    def GetColor2(self, colorID : int):
        c = ""
        if colorID == 10:
            c = self.white
        elif colorID == 0:
            c = self.black
        elif colorID == 1:
            c = self.red2
        elif colorID == 2:
            c = self.green2
        elif colorID == 3:
            c = self.blue2
        elif colorID == 4:
            c = self.yellow2
        elif colorID == 5:
            c = self.cyan2
        elif colorID == 6:
            c = self.magenta2
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










