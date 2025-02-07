import network
import socket
import time
import select
import leds

SSID = "Personal-861-2.4GHz" 
PASSWORD = "5YNECKk8hq"

print("corriendo...")


# Conectar a Wi-Fi
wlan = network.WLAN(network.STA_IF)
wlan.active(True)
wlan.connect(SSID, PASSWORD)

while not wlan.isconnected():
    time.sleep(1)

ip = wlan.ifconfig()[0]
print(f"Conectado a {SSID}, IP: {ip}")

# Crear servidor WebSocket (HTTP + WebSockets)
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((ip, 80))  # Puerto 80 para HTTP
server.listen(5)

print("Servidor Web corriendo...")

def handle_client(client):
    request = client.recv(1024)
    request = request.decode("utf-8")
    print("Petición recibida:", request)

    # Respuesta HTTP para la página web
    if "GET / " in request:
        response = """\
HTTP/1.1 200 OK
Content-Type: text/html

<!DOCTYPE html>
<html>
<head>
    <title>WebSocket Pico W</title>
</head>
<body>
    <h2>Envia un mensaje a la Pico W</h2>
    <input type="text" id="mensaje" placeholder="Escribe algo...">
    <button onclick="enviarMensaje()">Enviar</button>
    <p id="respuesta"></p>

    <script>
        function enviarMensaje() {
            var mensaje = document.getElementById("mensaje").value;
            fetch("/mensaje?data=" + encodeURIComponent(mensaje))
            .then(response => response.text())
            .then(data => document.getElementById("respuesta").innerText = data);
        }
    </script>
</body>
</html>
"""
        client.send(response.encode())
        client.close()

    elif "GET /mensaje?data=" in request:
        
        leds.Draw()
        time.sleep(1)
        leds.Reset()
        
        mensaje = request.split("GET /mensaje?data=")[1].split(" ")[0]
        mensaje = mensaje.replace("%20", " ")  # Decodificar espacios
        print(f"Mensaje recibido: {mensaje}")
        
        response = "HTTP/1.1 200 OK\nContent-Type: text/plain\n\nMensaje recibido!"
        client.send(response.encode())
        client.close()

while True:
    client, addr = server.accept()
    print(f"Cliente conectado desde {addr}")
    handle_client(client)
        
