

import network
import time
import ujson
import urequests


SSID = "Personal-861-2.4GHz" 
PASSWORD = "5YNECKk8hq"

wlan = network.WLAN(network.STA_IF)
wlan.active(True)
wlan.connect(SSID, PASSWORD)

while not wlan.isconnected():
    print("Conectando a WiFi...")
    time.sleep(1)

print("✅ Conectado a WiFi! IP:", wlan.ifconfig()[0])

# 📌 URL del servidor para obtener la hora
URL = "http://worldclockapi.com/api/json/utc/now"

def obtener_hora_http():
    """Obtiene la hora desde un servidor HTTP usando urequests."""
    try:
        response = urequests.get(URL)
        if response.status_code == 200:
            data = response.json()
            print("✅ Respuesta JSON:", data)  # Mostrar toda la respuesta para depuración
            
            datetime_str = data["currentDateTime"]
            print("Fecha y hora recibida:", datetime_str)  # Ver cómo viene la fecha

            # El formato de la fecha es "2025-02-09T13:30Z", vamos a extraer la hora
            try:
                hora = int(datetime_str[11:13])  # Hora es desde el índice 11 hasta el 13
                minutos = int(datetime_str[14:16])  # Minutos son desde el 14 hasta el 16
                segundos = 0  # No tenemos segundos explícitos, pero podemos asumir que es 00

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

# 📌 Obtener la hora
hora_actual = obtener_hora_http()
if hora_actual:
    print(f"🕒 Hora en UTC: {hora_actual[0]:02}:{hora_actual[1]:02}:{hora_actual[2]:02}")
else:
    print("❌ No se pudo obtener la hora.")
