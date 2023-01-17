import socket 
#import pickle

UDP_IP = "127.0.0.1"
UDP_PORT = 5555

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

#msg = "sample string!"
def Send(leds):
    message = ""
    total = len(leds)
    led = ""
    for a in range(total):
        led = str(leds[a])
        led = led.replace("(", "|")
        led = led.replace(")", "")
        led = led.replace(" ", "")
        message = message + led
    #message = pickle.dumps(leds)
    sock.sendto(message.encode(), (UDP_IP, UDP_PORT))
