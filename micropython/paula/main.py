from machine import Pin, UART
import time

# -----------------------
# Configuración DFPlayer
# -----------------------
uart = UART(1, baudrate=9600, tx=Pin(8), rx=Pin(9))
VOLUME_MAX = 25
VOLUME_MIN = 0
VOLUME_STEP = 2        # paso de volumen gradual
CHECK_INTERVAL = 0.2   # tiempo entre lecturas

def send_command(cmd, param=0):
    start = 0x7E
    version = 0xFF
    length = 0x06
    feedback = 0x00
    highByte = (param >> 8) & 0xFF
    lowByte = param & 0xFF
    end = 0xEF
    checksum = -(version + length + cmd + feedback + highByte + lowByte) & 0xFFFF
    c1 = (checksum >> 8) & 0xFF
    c2 = checksum & 0xFF
    packet = bytes([start, version, length, cmd, feedback,
                    highByte, lowByte, c1, c2, end])
    uart.write(packet)

# -----------------------
# Inicialización DFPlayer
# -----------------------
time.sleep(3)                # espera a que la SD esté lista
send_command(0x06, VOLUME_MIN)  # volumen inicial 0
send_command(0x03, 1)           # reproducir track 1
# Nota: no usamos 0x11, haremos loop manual usando BUSY

# -----------------------
# Configuración HC-SR04
# -----------------------
TRIG = Pin(2, Pin.OUT)
ECHO = Pin(3, Pin.IN)

def medir_distancia():
    TRIG.low()
    time.sleep_us(2)
    TRIG.high()
    time.sleep_us(10)
    TRIG.low()
    
    while ECHO.value() == 0:
        pass
    start = time.ticks_us()
    
    while ECHO.value() == 1:
        pass
    end = time.ticks_us()
    
    duracion = end - start
    distancia_cm = (duracion / 2) / 29.1
    return distancia_cm

# -----------------------
# Pin BUSY para loop
# -----------------------
BUSY = Pin(0, Pin.IN)

# -----------------------
# Loop principal
# -----------------------
volumen_actual = VOLUME_MIN

while True:
    # --- Control de distancia ---
    distancia = medir_distancia()
    if distancia < 50:
        volumen_objetivo = VOLUME_MAX
    else:
        volumen_objetivo = VOLUME_MIN

    # --- Ajuste gradual del volumen ---
    if volumen_actual < volumen_objetivo:
        volumen_actual = min(volumen_actual + VOLUME_STEP, VOLUME_MAX)
        send_command(0x06, volumen_actual)
    elif volumen_actual > volumen_objetivo:
        volumen_actual = max(volumen_actual - VOLUME_STEP, VOLUME_MIN)
        send_command(0x06, volumen_actual)

    # --- Loop manual del track ---
    # Si BUSY está HIGH (no reproduce), reinicia track 1
    if BUSY.value() == 1:
        send_command(0x03, 1)
    
    # --- Debug ---
    print("Distancia: {:.1f} cm | Volumen: {} | BUSY: {}".format(distancia, volumen_actual, BUSY.value()))
    
    time.sleep(CHECK_INTERVAL)
