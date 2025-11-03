from machine import Pin, UART
import time

# UART para comandos al DFPlayer
uart = UART(1, baudrate=9600, tx=Pin(8), rx=Pin(9))



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
    packet = bytes([start, version, length, cmd, feedback, highByte, lowByte, c1, c2, end])
    uart.write(packet)

time.sleep(2)

# Subir volumen
send_command(0x06, 25)

# Reproducir track 1
send_command(0x03, 1)

# Leer el pin BUSY
while True:
    time.sleep(0.5)

