from machine import ADC, Pin
pot1 = ADC(28)
pot2 = ADC(27)
button1 = Pin(14, Pin.IN)

def UpdatePot():
    global pot1_value
    global pot2_value
    pot_min = 256
    pot_max = 65535    
    value1 = pot1.read_u16();
    pot1_value = (value1 - pot_min)/(pot_max - pot_min)
    value2 = pot2.read_u16();
    pot2_value = (value2 - pot_min)/(pot_max - pot_min)