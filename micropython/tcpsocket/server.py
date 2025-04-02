import network
import socket
import time
import select
import leds
import ujson

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
        
        
        



wlan = network.WLAN(network.STA_IF)
wlan.active(True)
wlan.connect(SSID, PASSWORD)

while not wlan.isconnected():
    print("Conectando a WiFi...")
    time.sleep(1)

print("Conectado! IP:", wlan.ifconfig()[0])

HOST = "213.188.196.246"
URL = "/api/Time/current/zone?timeZone=America/Argentina/Buenos_Aires"

def obtener_hora_http():
    """Obtiene la hora desde worldtimeapi.org usando un socket TCP."""
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.settimeout(10)  # Esperar hasta 10 segundos

    try:
        print(f"Conectando a {HOST}...")
        sock.connect((HOST, 80))  # Conectar al servidor HTTP en el puerto 80

        request = f"GET {URL} HTTP/1.1\r\nHost: {HOST}\r\nConnection: close\r\n\r\n"
        sock.send(request.encode())

        response = b""  # Almacenar la respuesta completa
        while True:
            chunk = sock.recv(1024)  # Recibir en bloques de 1024 bytes
            if not chunk:
                break
            response += chunk

        response = response.decode()

        # 📌 Verificar si la respuesta es válida
        if "200 OK" not in response:
            print("⚠️ Error en la respuesta HTTP:", response)
            return None

        # 📌 Buscar el inicio del JSON
        json_start = response.find("{")
        if json_start == -1:
            print("⚠️ No se encontró JSON en la respuesta")
            return None

        json_data = response[json_start:]  # Extraer solo el JSON
        data = ujson.loads(json_data)  # Convertir a diccionario

        datetime_str = data["datetime"]  # Obtener la hora en formato ISO 8601
        
        print("entonces : ", datetime_str.date)

        # 📌 Extraer hora, minutos y segundos
        hora = int(datetime_str[11:13])
        minutos = int(datetime_str[14:16])
        segundos = int(datetime_str[17:19])

        return hora, minutos, segundos

    except Exception as e:
        print("🚨 Error obteniendo la hora:", e)
        return None
    finally:
        sock.close()

# 📌 Obtener la hora
hora_actual = obtener_hora_http()
if hora_actual:
    print(f"Hora en Argentina: {hora_actual[0]:02}:{hora_actual[1]:02}:{hora_actual[2]:02}")
else:
    print("❌ No se pudo obtener la hora.")






while True:
    client, addr = server.accept()
    print(f"Cliente conectado desde {addr}")
    handle_client(client)
    # 📌 Obtener la hora

        
    
    
    
    
    
    
    
    
    
    
    
    



        
