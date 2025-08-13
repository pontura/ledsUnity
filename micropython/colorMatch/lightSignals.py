import time, random, machine, neopixel

NUM_LEDS = 288
PIN = 22
np = neopixel.NeoPixel(machine.Pin(PIN), NUM_LEDS)

# Paleta de colores vivos (podés agregar más)
PALETA = [
    (255, 0, 0),     # Rojo
    (255, 165, 0),   # Naranja
    (255, 255, 0),   # Amarillo
    (0, 255, 0),     # Verde
    (0, 255, 255),   # Cian
    (0, 0, 255),     # Azul
    (255, 0, 255),   # Magenta
    (255, 105, 180), # Rosa
    (255, 255, 255)  # Blanco
]

def confeti_colores(decay=0.85, speed=0.02):
    leds = [(0, 0, 0)] * NUM_LEDS
    while True:
        # Desvanecer
        for i in range(NUM_LEDS):
            leds[i] = tuple(int(c * decay) for c in leds[i])
        # Crear varios destellos nuevos por frame
        for _ in range(5):  # Cantidad de nuevos destellos por frame
            pos = random.randint(0, NUM_LEDS - 1)
            color = random.choice(PALETA)
            leds[pos] = color
        # Mostrar
        for i in range(NUM_LEDS):
            np[i] = leds[i]
        np.write()
        time.sleep(speed)

confeti_colores()
