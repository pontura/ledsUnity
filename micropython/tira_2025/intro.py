import time
import random
import math

class Intro:

    numpix = 300
    sparks = []    

    spawn_rate = 0.12
    spawn_timer = 0
    
    timer = 0
    timerToAutomaticPlay = 11

    flame_time = 0  # para animar la llama

    def Init(self, game, numpix):
        self.timer = 0
        self.game = game
        self.numpix = numpix
        self.sparks = []
        self.spawn_timer = 0
        self.flame_time = 0


    def SpawnSpark(self):
        center = self.numpix // 2
        pos = float(center)

        vel = 0.0

        accel = random.uniform(100.0, 250.0)
        accel *= 1 if random.random() < 0.5 else -1

        max_life = random.uniform(0.6, 1.4)

        self.sparks.append([pos, vel, accel, max_life, max_life])


    def DrawCenterFlame(self, dt):
        """
        Dibuja los 4 LEDs centrales con un efecto de llama.
        """
        center = self.numpix // 2

        self.flame_time += dt * 6.0  # velocidad de oscilación

        # brillo oscilante entre 0.6 y 1.0
        base_flame = 0.6 + (math.sin(self.flame_time) * 0.4 + 0.4)

        # 4 LEDs centrales
        flame_positions = [center - 2, center - 1, center, center + 1]

        for i, pix in enumerate(flame_positions):

            # cuanto más lejos del centro, menos brillo → tipo llama real
            falloff = 1.0 - (abs(i - 1.5) * 0.3)

            brightness = base_flame * falloff

            self.game.SetLedAlpha(pix, 10, brightness)


    def OnUpdate(self, dt):
        self.timer = self.timer + dt
        
        if self.timer>self.timerToAutomaticPlay:
                  
            self.v = 0.05
            self.timer = 0
            self.game.Fade(4, 2)
        else:

            # limpiar leds
            for i in range(self.numpix-1):
                self.game.SetLedAlpha(i, 10, 0)

            # ---- Llama central fija ----
            self.DrawCenterFlame(dt)

            # ---- Chispas continuas ----
            self.spawn_timer += dt
            while self.spawn_timer >= self.spawn_rate:
                self.spawn_timer -= self.spawn_rate
                self.SpawnSpark()

            new_sparks = []
            for pos, vel, accel, life, max_life in self.sparks:

                # acelerar al principio
                vel += accel * dt
                pos += vel * dt

                # fricción suave
                accel *= 0.92

                # vida de la chispa
                life -= dt

                brightness = max(0.0, life / max_life)
                pix = int(pos)

                # dibujar chispa
                if 0 <= pix < self.numpix:
                    self.game.SetLedAlpha(pix, 10, brightness)

                # conservar chispa viva
                if life > 0 and 0 <= pix < self.numpix:
                    new_sparks.append([pos, vel, accel, life, max_life])

            self.sparks = new_sparks
            time.sleep(0.001)

       

