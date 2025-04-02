import time
import random
from machine import Pin, SPI
import apa102

# Configuración básica
TOTAL_PIXELS = 60  # Típico para tiras LED
CENTER = TOTAL_PIXELS // 2
FRAME_RATE = 60
FRAME_DELAY = 1 / FRAME_RATE

# Configuración del juego
INIT_CARS_IN = 5.0
MIN_CURVE_POSSIBLE = 25
MIN_CURVE_POSSIBLE_MAX = 150

class Pixel:
    def __init__(self):
        self.color = (0, 0, 0)
        self.brightness = 0.0
    
    def set_data(self, color, alpha):
        self.color = color
        self.brightness = alpha
    
    def is_available(self):
        return self.brightness < 0.1

class RoadPoint:
    def __init__(self):
        self.road_pixel_width = 0
        self.alpha_value = 0.25
        self.initial_x = 0.0
        self.x = 0.0
        self.width = 0.0
        self.car_x = 0.0
    
    def in_position(self):
        return self.width > self.road_pixel_width
    
    def update_car(self):
        if self.alpha_value == 0.25:
            self.alpha_value = 0.75
        elif self.alpha_value == 0.75:
            self.alpha_value = 0.25
    
    def alpha(self):
        if self.width > self.road_pixel_width - 30:
            return 1.0
        elif self.width > self.road_pixel_width - 60:
            return 0.7
        elif self.width > self.road_pixel_width - 100:
            return 0.5
        else:
            return self.alpha_value
    
    def add_car(self, road_pixel_width):
        self.road_pixel_width = road_pixel_width
        self.car_x = random.uniform(0.1, 0.9)
    
    def set_off(self):
        self.car_x = 0.0

class PixelsManager:
    def __init__(self):
        # Configuración de la tira LED (APA102)
        self.spi = SPI(0, baudrate=8000000, polarity=0, phase=1)
        self.led_strip = apa102.APA102(self.spi, TOTAL_PIXELS)
        
        self.pixels = [Pixel() for _ in range(TOTAL_PIXELS)]
        self.road_points = []
        self.state = -1  # 0 = playing, 1 = die
        
        # Configuración del juego
        self.cars_random_limits = (1, 5)
        self.cars_random = (0, 0)
        self.min_cars_random = (0.2, 0.75)
        self.cars_random_disminution = 0.05
        
        self.car_passed = 0
        self.road_pixel_width_limits = (TOTAL_PIXELS, 10)
        self.road_pixel_width = self.road_pixel_width_limits[0]
        self.road_pixel_width_decrease = 1
        self.timer = 0
        self.distance_between_points = 0.3
        
        self.speed = 10
        self.aceleration = 1.02
        self.speed_increase = 1
        self.speed_limits = (10, 20)
        self.aceleration_limits = (1.02, 1.04)
        
        self.random_to_curve_duration = (5, 10)
        self.vanishing_point = CENTER
        self.vanishing_point_target = CENTER
        
        self.car_pos = CENTER
        self.car_movement = 0
        self.distance = 0
        self.direction = 0
        self.car_speed = 1
        
        self.crash_timer = 0
        self.crash_loops = 0
        
        self.last_right_keyframe = 0
        self.limits_list_right = 0
        self.limits_list_left = 0
        self.limits_list_right_goto = 0
        self.limits_list_left_goto = 0
        
        self.restart()
    
    def restart(self):
        self.cars_random = self.cars_random_limits
        self.state = 0
        self.road_pixel_width = self.road_pixel_width_limits[0]
        self.timer = 0
        self.distance = 0
        self.speed = self.speed_limits[0]
        self.aceleration = self.aceleration_limits[0]
        self.car_pos = CENTER
        self.car_movement = 0
        self.road_points = []
        self.vanishing_point = CENTER
        
        self.set_next_path()
        time.sleep(INIT_CARS_IN)
        self.add_car()
    
    def update_playing(self):
        frame_time = FRAME_DELAY
        self.distance += frame_time
        self.timer += frame_time
        
        if self.timer > self.distance_between_points:
            self.add_road_point()
        
        self.update_road_points()
        self.draw()
        self.set_vanishing_point()
        
        if self.road_pixel_width <= self.road_pixel_width_limits[1]:
            self.road_pixel_width = self.road_pixel_width_limits[1]
        else:
            self.road_pixel_width -= self.road_pixel_width_decrease * frame_time
        
        if self.speed >= self.speed_limits[1]:
            self.speed = self.speed_limits[1]
        self.speed += (self.speed_increase * frame_time) / 10
        
        if self.aceleration >= self.aceleration_limits[1]:
            self.aceleration = self.aceleration_limits[1]
        self.aceleration += (self.speed_increase * frame_time) / 1000
    
    def add_car(self):
        if self.road_points:
            self.road_points[-1].add_car(self.road_pixel_width)
            delay = random.uniform(self.cars_random[0], self.cars_random[1])
            time.sleep(delay)
            self.add_car()
            
            # Actualizar límites aleatorios
            new_x = max(self.cars_random[0] - self.cars_random_disminution, self.min_cars_random[0])
            new_y = max(self.cars_random[1] - self.cars_random_disminution, self.min_cars_random[1])
            self.cars_random = (new_x, new_y)
    
    def add_road_point(self):
        self.timer = 0
        rp = RoadPoint()
        rp.initial_x = self.vanishing_point
        rp.x = rp.initial_x
        rp.width = 1
        self.road_points.append(rp)
    
    def update_road_points(self):
        to_remove = None
        for rp in self.road_points:
            rp.width += self.speed * FRAME_DELAY
            rp.width *= self.aceleration
            rp.x = rp.initial_x + (rp.width * (CENTER - rp.initial_x) / TOTAL_PIXELS)
            if rp.width > TOTAL_PIXELS:
                to_remove = rp
        
        if to_remove is not None:
            self.road_points.remove(to_remove)
    
    def draw(self):
        # Limpiar todos los píxeles
        self.set_all_pixels_to((0, 0, 0), 0)
        
        # Dibujar la carretera y coches
        road_pixel_id = 0
        road_x = 0
        id_num = len(self.road_points)
        
        for rp in self.road_points:
            if road_pixel_id == 0 and rp.width < self.road_pixel_width:
                road_pixel_id = id_num
                color = (255, 0, 0)  # Rojo
                alpha = 1
                road_x = rp.x / CENTER
            elif id_num < road_pixel_id:
                color = (0, 0, 255)  # Azul
                alpha = 0.15 + (rp.width / self.road_pixel_width)
                self.set_road_point(rp, color, alpha, 0, 0)
            else:
                if self.car_passed > 0:
                    color = (255, 0, 0)  # Rojo
                    alpha = 1
                    self.car_passed += FRAME_DELAY
                    if self.car_passed > 1.5:
                        self.car_passed = 0
                else:
                    color = (255, 255, 255)  # Blanco
                    alpha = (rp.width - self.road_pixel_width) / (TOTAL_PIXELS - self.road_pixel_width)
                self.set_road_point(rp, color, alpha)
            
            # Dibujar coches
            if rp.car_x != 0:
                car_on_position = rp.in_position()
                rp.update_car()
                pixel = int(rp.x - (rp.width / 2) + rp.width * rp.car_x)
                car_alpha = rp.alpha()
                car_color = (255, 0, 0)  # Rojo
                red_dark = (64, 0, 0)
                
                if rp.width > self.road_pixel_width - 40:
                    # Dos luces
                    self.set_color(pixel + 5, car_color, 1)
                    self.set_color(pixel + 4, car_color, 1)
                    self.set_color(pixel - 4, car_color, 1)
                    self.set_color(pixel - 5, car_color, 1)
                elif rp.width > self.road_pixel_width - 80:
                    self.set_color(pixel + 3, car_color, car_alpha)
                    self.set_color(pixel - 3, car_color, car_alpha)
                elif rp.width > self.road_pixel_width - 130:
                    self.set_color(pixel + 1, car_color, car_alpha)
                    self.set_color(pixel - 1, car_color, car_alpha)
                else:
                    self.set_color(pixel, car_color, car_alpha)
                
                if car_on_position:
                    rp.set_off()
                    self.car_passed = 1
                    if self.car_pos >= pixel - 5 and self.car_pos <= pixel + 5:
                        self.crash()
            
            id_num -= 1
        
        # Dibujar coche del jugador
        self.set_color(int(self.car_pos), (255, 255, 0), 1)  # Amarillo
        
        # Actualizar LEDs
        self.update_leds()
    
    def set_color(self, pixel, color, alpha):
        if 0 <= pixel < TOTAL_PIXELS:
            self.pixels[pixel].set_data(color, alpha)
    
    def set_all_pixels_to(self, color, alpha):
        for pixel in self.pixels:
            pixel.set_data(color, alpha)
    
    def set_road_point(self, rp, color, alpha, offset=0, priority=1):
        pixel_right = int(rp.x + (rp.width / 2)) + offset
        pixel_left = int(rp.x - (rp.width / 2)) - offset
        
        if priority == 0:
            if 0 <= pixel_right < TOTAL_PIXELS and self.pixels[pixel_right].is_available():
                self.set_color(pixel_right, color, alpha)
            if 0 <= pixel_left < TOTAL_PIXELS and self.pixels[pixel_left].is_available():
                self.set_color(pixel_left, color, alpha)
            return
        
        self.set_color(pixel_right, color, alpha)
        self.set_color(pixel_left, color, alpha)
    
    def update_leds(self):
        for i, pixel in enumerate(self.pixels):
            r, g, b = pixel.color
            brightness = int(pixel.brightness * 31)  # APA102 usa 0-31 para brillo
            self.led_strip.set_pixel(i, r, g, b, brightness)
        self.led_strip.show()
    
    def move(self, value):
        if self.distance < 2:
            value = 0
        if self.state == 1:
            value = 0
        self.direction = value
        self.car_pos -= self.car_speed * value * FRAME_DELAY
        self.car_pos = max(0, min(TOTAL_PIXELS - 1, self.car_pos))
    
    def crash(self):
        if self.distance < 4 or self.state == 1:
            return
        self.crash_timer = 0
        self.state = 1
        self.crash_loops = 0
    
    def update_crash(self):
        self.crash_timer += FRAME_DELAY
        if self.crash_loops > 5:
            self.restart()
        else:
            if self.crash_timer > 0.3:
                self.crash_loops += 1
                self.crash_timer = 0
            if self.crash_timer > 0.15:
                self.draw()
            else:
                self.set_all_pixels_to((255, 0, 0), 1)
                self.update_leds()

# Ejemplo de uso
if __name__ == "__main__":
    game = PixelsManager()
    try:
        while True:
            # Simular entrada de usuario (deberías reemplazar esto con controles reales)
            game.move(random.uniform(-1, 1))
            game.update_playing()
            time.sleep(FRAME_DELAY)
    except KeyboardInterrupt:
        game.led_strip.clear_strip()
        game.led_strip.show()