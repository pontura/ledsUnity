import network
import time
import ujson
import urequests
import leds

SSID = "Personal-861-2.4GHz" 
PASSWORD = "5YNECKk8hq"

wlan = network.WLAN(network.STA_IF)
wlan.active(True)
wlan.connect(SSID, PASSWORD)

while not wlan.isconnected():
    print("Conectando a WiFi...")
    time.sleep(1)

print("✅ Conectado a WiFi! IP:", wlan.ifconfig()[0])

# 📌 URL del servidor para obtener la hora en la zona horaria de Argentina
# Reemplaza 'TU_API_KEY' con tu clave API de timezonedb
API_KEY = "BBAGOE67MF5J"
URL = f"http://api.timezonedb.com/v2.1/get-time-zone?key={API_KEY}&format=json&by=zone&zone=America/Argentina/Buenos_Aires"

def obtener_hora_http():
    """Obtiene la hora desde un servidor HTTP usando urequests."""
    try:
        response = urequests.get(URL)
        print(f"⚠️ Código de respuesta HTTP: {response.status_code}")
        print(f"⚠️ Respuesta completa: {response.text}")
        
        if response.status_code == 200:
            data = response.json()
            print("✅ Respuesta JSON:", data)  # Mostrar toda la respuesta para depuración
            
            datetime_str = data["formatted"]
            print("Fecha y hora recibida:", datetime_str)  # Ver cómo viene la fecha

            # El formato de la fecha es "2025-02-09 13:30:00", vamos a extraer la hora
            try:
                hora = int(datetime_str[11:13])  # Hora es desde el índice 11 hasta el 13
                minutos = int(datetime_str[14:16])  # Minutos son desde el 14 hasta el 16
                segundos = int(datetime_str[17:19])  # Segundos son desde el 17 hasta el 19

                return hora, minutos, segundos
            except ValueError as e:
                print(f"🚨 Error al procesar la hora: {e}")
                return None
        else:
            print(f"⚠️ Error HTTP: {response.status_code}")
            return None
    except Exception as e:
        print("🚨 Error obteniendo la hora HTTP:", e)
        return None

state = "loading"
hour = 0
min = 0
sec = 0

def Refresh():
    hora_actual = obtener_hora_http()
    if hora_actual:
        global state 
        global hour 
        global min 
        global sec 
        hour = hora_actual[0]
        min = hora_actual[1]
        sec = hora_actual[2]
        state = "playing"
        print("REFRESHED hour:", hour, "  min:" , min , "  sec: ", sec, " state: ", state)
    else:
        print("❌ No se pudo obtener la hora.")
        
lastSec = 0
Refresh()
framerate = 0.25
while True:
    if state == "playing":
        sec = sec + framerate
        if round(sec) !=  round(lastSec):
            print("sec", sec)
            lastSec = sec
            if sec>=60:
                sec = 0
                min = min +1
                if min>=60:                    
                    Refresh()
                    min = 0
                    hour = hour + 1                
                    if hour>=24:
                        hour = 0                    
        leds.Draw()
        leds.Hours(hour)
        leds.Min(min)
        leds.Secs(sec)
        leds.Send()
        
        print("hour:", hour, "  min:" , min , "  sec: ", sec)
    
    time.sleep(framerate) 
        
