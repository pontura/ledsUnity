from machine import ADC, Pin
import time
pot1 = ADC(28)
pot2 = ADC(27)
button1 = Pin(14, Pin.IN)

def UpdatePot():
    global pot1_value
    global pot2_value
    global v1
    global v2
    
    pot_min = 256
    pot_max = 65535    
    
    v1_ = pot1.read_u16()
    v2_ = pot2.read_u16()    
    
    v1 = lerp(v1_, pot1.read_u16(), 0.05)
    v2 = lerp(v2_, pot2.read_u16(), 0.05)
    
    pot1_value = (v1 - pot_min)/(pot_max - pot_min)
    pot2_value = (v2 - pot_min)/(pot_max - pot_min)
    pot1_value = (pot1_value*2)-1
    pot2_value = (pot2_value*2)-1
    
    print(pot1_value, "     ", pot2_value)


def lerp(a: float, b: float, t: float) -> float:
    return (1 - t) * a + t * b

while True:
    UpdatePot()
    time.sleep(0.1)      