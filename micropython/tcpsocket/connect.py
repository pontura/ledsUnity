import network
import socket
import time

SSID = "Personal-861-2.4GHz"  # Cambia por el nombre de tu Wi-Fi
PASSWORD = "5YNECKk8hq"     # Cambia por la contraseña de tu Wi-Fi
 
# Conectar a Wi-Fi
wlan = network.WLAN(network.STA_IF)
wlan.active(True)
wlan.connect(SSID, PASSWORD)

# Esperar conexión
while not wlan.isconnected():
    time.sleep(1)

print(f"Conectado a {SSID}, IP: {wlan.ifconfig()[0]}")

# Crear servidor TCP
# IP de la Pico: 192.168.1.29
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((wlan.ifconfig()[0], 12345))  # Puerto 12345
server.listen(1)

print("Esperando conexión...")

conn, addr = server.accept()
print(f"Cliente conectado desde: {addr}")

while True:
    data = conn.recv(1024)
    if not data:
        break
    print(f"Recibido: {data.decode()}")
    conn.sendall(b"Mensaje recibido!")  # Respuesta al cliente

conn.close()
server.close()