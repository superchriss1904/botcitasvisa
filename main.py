import requests
from bs4 import BeautifulSoup
import time

# Configura tus datos
TELEGRAM_TOKEN = "7824972217:AAEt15IE6lyLnNfwoj8UUunZ6wOS7IVmM20"
TELEGRAM_CHAT_ID = "1755649442"
URL = "https://ais.usvisa-info.com/es-mx/niv/schedule/69245614/appointment"

# Intervalo de tiempo en segundos (10 minutos)
INTERVALO = 600

def enviar_mensaje(texto):
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    payload = {"chat_id": TELEGRAM_CHAT_ID, "text": texto}
    requests.post(url, data=payload)

def obtener_fecha_disponible():
    headers = {
        "User-Agent": "Mozilla/5.0",
        "Accept-Language": "es-MX",
    }

    try:
        response = requests.get(URL, headers=headers)
        soup = BeautifulSoup(response.text, "html.parser")
        texto = soup.get_text()

        for linea in texto.splitlines():
            if "La fecha más temprana disponible es" in linea:
                return linea.strip()
        return None
    except Exception as e:
        print(f"Error al obtener la página: {e}")
        return None

def cargar_fecha_anterior():
    try:
        with open("ultima_fecha.txt", "r", encoding="utf-8") as f:
            return f.read().strip()
    except FileNotFoundError:
        return ""

def guardar_fecha_nueva(fecha):
    with open("ultima_fecha.txt", "w", encoding="utf-8") as f:
        f.write(fecha)

# --- Monitoreo principal ---
print("Iniciando monitoreo de citas")

while True:
    fecha_actual = obtener_fecha_disponible()
    fecha_guardada = cargar_fecha_anterior()

    if fecha_actual and fecha_actual != fecha_guardada:
        mensaje = f"📅 ¡Nueva cita disponible!\n\n{fecha_actual}\n\n🔗 {URL}"
        enviar_mensaje(mensaje)
        guardar_fecha_nueva(fecha_actual)
        print("🟢 Aviso enviado:", fecha_actual)
    else:
        print("🔄 Sin cambios. Última fecha:", fecha_guardada)

    time.sleep(INTERVALO)
