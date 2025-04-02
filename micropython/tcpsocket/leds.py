import machine
import neopixel
import time

# Configuración
PIN_WS2812 = 22  # Pin GPIO donde está conectada la tira
NUM_LEDS = 240   # Número de LEDs en la tira
hours = NUM_LEDS/24

# Inicializar la tira de LEDs
np = neopixel.NeoPixel(machine.Pin(PIN_WS2812), NUM_LEDS)
    
def Draw():
    """Pinta la primera mitad de rojo y la segunda mitad de azul."""
    
    ledNum = 0
    hour = 0
    for i in range(NUM_LEDS):
        if ledNum == 0:
            if hour % 3 == 0:                
                np[i] = (255, 255, 255)  # horas
            else:                
                np[i] = (5, 5, 5)  # horas
            hour = hour +1
        else:
            np[i] = (0, 0, 0)  # nada
        ledNum = ledNum+1
        if ledNum>=hours:
            ledNum = 0
            
    #np.write()  # Enviar datos a la tira
    print("leds on")
    
def Reset():    
    mitad = NUM_LEDS
    for i in range(NUM_LEDS):
        np[i] = (0, 0, 0)  # Rojo
    np.write()  # Enviar datos a la tira
    print("leds off")
    
def Hours(n):
    num = round(n*hours)
    print("Hours " , num)
    np[num] = (255, 0, 0)  # Rojo
    
def Min(n):
    num = round(n*NUM_LEDS/60)
    print("Min " , num)
    np[num] = (0, 0, 255)  # Rojo
    
def Secs(n):
    num = round(n*NUM_LEDS/60)
    print("Secs " , num)
    np[num] = (0, 255, 0)  # Rojo
    
def Send():
    np.write()  # Enviar datos a la tira
    

#Reset()
