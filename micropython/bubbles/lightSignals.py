import machine
import neopixel
import time
import random

class LightSignals:
    def __init__(self, pin_num=1, num_pixels=100):
        self.num_pixels = num_pixels
        self.pin = machine.Pin(pin_num)
        self.strip = neopixel.NeoPixel(self.pin, self.num_pixels)
        self.current_colors = [(0, 0, 0)] * num_pixels  # Para guardar el estado actual

    def transition_range(self, start, end, new_color, delay_ms=10):
        for i in range(start, end):
            self.strip[i] = new_color
            self.current_colors[i] = new_color  # Actualizamos estado
            self.strip.write()
            time.sleep_ms(delay_ms)

    def update_groups(self, color1, color2, delay_ms=10):
        # Transición del primer grupo (0-8)
        self.transition_range(0, 9, color1, delay_ms)
        # Transición del segundo grupo (9-17)
        self.transition_range(9, 18, color2, delay_ms)

v = 100
def random_color():
    rand = random.randint(0, 6)
    if  rand== 0:
        return (v,0,0)
    elif rand == 1:
        return (0, v,0)
    elif rand == 2:
        return (0,0,v)
    elif rand== 3:
        return (v,v,0)
    elif rand == 4:
        return (0, v,v)
    else:
        return (v,0,v)

# --- Uso ---

pixels = LightSignals(pin_num=1)

while True:
    color1 = random_color()
    color2 = random_color()

    pixels.update_groups(color1, color2)

    time.sleep(2)
    print ("hola")
