import machine
import neopixel
import time

# Configuración
NUM_PIXELS = 20
PIN = 0  # GPIO0

# Inicializar la tira de LEDs
np = neopixel.NeoPixel(machine.Pin(PIN), NUM_PIXELS)

# Encender los primeros 10 en verde
for i in range(10):
    np[i] = (0, 255, 0)  # (R, G, B)

# Encender los últimos 10 en rojo
for i in range(10, 20):
    np[i] = (255, 0, 0)

# Mostrar el cambio
np.write()
