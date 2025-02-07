import network
import time

def connect_to_wifi(ssid, password):
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    if not wlan.isconnected():
        print('Conectando a la red...')
        wlan.connect(ssid, password)
        while not wlan.isconnected():
            time.sleep(1)
    print('Conexión establecida. Dirección IP:', wlan.ifconfig()[0])
    return wlan.ifconfig()[0]

# Cambia "TuSSID" y "TuContraseña" por tus credenciales Wi-Fi

connect_to_wifi("Personal-861-5GHz", "5YNECKk8hq")