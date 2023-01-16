from machine import Pin
import rp2

all = []

PIN_NUM = 22

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

def Update(NUM_LEDS):    
    dimmer_ar = array.array("I", [0 for _ in range(NUM_LEDS)])
    
def SetLeds(dimmer_ar, NUM):    
    sm.put(dimmer_ar,NUM)
    
def SetPixel(dimmer_ar, color, id):
    c = setColor(color)
    r = int(((c >> 8) & 0xFF) )
    g = int(((c >> 16) & 0xFF))
    b = int((c & 0xFF) )
    dimmer_ar[id] = (g<<16) + (r<<8) + b
    
def SetPixelBrighteness(dimmer_ar, color, id, brightness):
    c = setColor(color)
    r = int(((c >> 8) & 0xFF) * brightness )
    g = int(((c >> 16) & 0xFF) * brightness)
    b = int((c & 0xFF) * brightness)
    dimmer_ar[id] = (g<<16) + (r<<8) + b    
   
   
BLACK = (0, 0, 0)
RED = (255, 0, 0)
YELLOW = (255, 150, 0)
GREEN = (0, 255, 0)

def setColor(color):
    return (color[1]<<16) + (color[0]<<8) + color[2]

