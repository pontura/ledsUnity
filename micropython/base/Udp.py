import socket 

UDP_IP = "127.0.0.1"
UDP_PORT = 5555

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

msg = "sample string!"

sock.sendto(msg.encode(), (UDP_IP, UDP_PORT))