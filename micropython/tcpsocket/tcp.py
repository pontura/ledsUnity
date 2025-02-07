import socket
from wifi_connect import connect_to_wifi

# Conecta a Wi-Fi
ip = connect_to_wifi("Personal-861-5GHz", "5YNECKk8hq")

# Configura el servidor TCP
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind((ip, 8080))  # IP y puerto del servidor
server_socket.listen(1)

print("Esperando conexión en:", ip, "puerto 8080")

while True:
    client_socket, client_address = server_socket.accept()
    print("Conexión aceptada de:", client_address)
    data = client_socket.recv(1024)  # Recibe datos del cliente
    print("Datos recibidos:", data.decode())
    client_socket.send("Mensaje recibido".encode())  # Responde al cliente
    client_socket.close()
