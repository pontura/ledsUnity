import time
from machine import ADC, Pin
pot1 = ADC(27)

def UpdatePot():
    while True:
        value1 = pot1.read_u16();
        print (value1)
        time.sleep(0.2)
        
UpdatePot()