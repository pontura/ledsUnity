import machine
import neopixel
import time

# Configuración
PIN_WS2812 = 22  # Pin GPIO donde está conectada la tira
NUM_LEDS = 240   # Número de LEDs en la tira

# Inicializar la tira de LEDs
np = neopixel.NeoPixel(machine.Pin(PIN_WS2812), NUM_LEDS)
    
def Draw():
    """Pinta la primera mitad de rojo y la segunda mitad de azul."""
    mitad = NUM_LEDS
    for i in range(mitad):
        np[i] = (255, 0, 0)  # Rojo
    np.write()  # Enviar datos a la tira
    print("leds on")
    
def Reset():    
    mitad = NUM_LEDS
    for i in range(mitad):
        np[i] = (0, 0, 0)  # Rojo
    np.write()  # Enviar datos a la tira
    print("leds off")
