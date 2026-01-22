import tls_client
import time
import random
import datetime
import threading
import requests
import os
from flask import Flask
from itertools import cycle

# --- CONFIGURACIÓN TELEGRAM (Tus datos ya puestos) ---
TELEGRAM_BOT_TOKEN = "8512201629:AAFYKnKttqURljq28VB3yjrdpK4HwFsSf2I" 
TELEGRAM_CHAT_ID = "-5172904911" 

# --- CONFIGURACIÓN DE TIEMPO ---
MIN_MINUTOS = 31
MAX_MINUTOS = 36

# --- TUS MENSAJES ---
LISTA_MENSAJES = [
    "🚀 **ONLY $75 USD – LIMITED TIME ➤** Config Cloud + OpenBullet Guide (113 Pages) | Web & App Configs step-by-step from scratch 🔥 **➜** https://t.me/myConfigCloud",
    "🔥🦠 $50 USD LIFETIME! ➤ 140+ Auto-Updating Configs for Openbullet & Silverbullet ➤ Accepting Custom Requests - https://t.me/myConfigCloud",
    "⚡ **START NOW – PAY LATER ➤** Cracking E-Book + Config Cloud | **Learn Web & App configs from 0, sell your own work, get 155+ auto-updated configs** https://t.me/myConfigCloud"
]

mensajes_rotativos = cycle(LISTA_MENSAJES)

# --- CONFIGURACIÓN DE HEADERS ---
URL = "https://chat2.patched.to/message/marketplace"
HEADERS = {
    "accept": "application/json, text/plain, */*",
    "accept-language": "es-AR,es;q=0.9,en-US;q=0.8,en;q=0.7,es-419;q=0.6",
    # Tu token de autorización
    "authorization": "eyJ1aWQiOjM0NjMyLCJhdmF0YXIiOiIuXC91cGxvYWRzXC9hdmF0YXJzXC9hdmF0YXJfMzQ2MzIucG5nP2RhdGVsaW5lPTE3NjY0MjQwMzkiLCJiYW5uZXIiOiIiLCJ0aXRsZSI6Ilx1ZDgzZVx1ZGM4MiBodHRwczpcL1wvdmlydXNudG8uY29tIFx1ZDgzZVx1ZGM4MCIsInVzZXJuYW1lIjoiVmlydXNOVE8iLCJncm91cCI6eyJpZCI6MiwiaW1hZ2UiOiJodHRwczpcL1wvY2RuLnBhdGNoZWQuc2hcL3JhbmtzXC9tZW1iZXIucG5nIn0sImljb24iOiJcL2ltYWdlc1wvYXNzZXRzXC9pdGVtc1wvZmxhZ3NcL2FyZ2VudGluYS5wbmciLCJzb2NpYWwiOnsiZGlzY29yZCI6Indob2lzbWF0dGhldyIsInRlbGVncmFtIjoiQHdob2lzX3R5bGVyIn0sIm5hbWVzdHlsZSI6IjxzcGFuIHN0eWxlPVwiY29sb3I6IHJnYmEoMjU1LDI1NSwyNTUsMC45MCk7XCI-PHN0cm9uZz5WaXJ1c05UTzxcL3N0cm9uZz48XC9zcGFuPiIsInN0YXRpc3RpY3MiOnsicG9zdCI6MTA5NSwidGhyZWFkIjozMn0sImV4cGlyZWQiOjE3NjkwNTc1MjV9.2yYS9Z9A7Ws.XVXsWHuE5d_ptIjahhH2uak8uW7e8xHoobkZLdatkUrThaSauydIW0NoZGf6Wpu8yrjYfK1wZ0Izqn1sNh0MBw",
    "content-type": "application/json",
    "origin": "https://patched.to",
    "referer": "https://patched.to/",
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/144.0.0.0 Safari/537.36",
    "x-api-key": "28c58f7376e44cdfb0f012039a82d13f"
}

# --- SERVIDOR FLASK ---
app = Flask(__name__)

@app.route('/')
def home():
    return "Bot Patch.to Activo - UptimeRobot OK"

# --- FUNCIONES ---
def notificar_telegram(mensaje):
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    payload = {
        "chat_id": TELEGRAM_CHAT_ID,
        "text": mensaje,
        "parse_mode": "HTML"
    }
    try:
        requests.post(url, json=payload, timeout=10)
    except Exception as e:
        print(f"Error Telegram: {e}", flush=True)

def enviar_shout():
    mensaje_a_enviar = next(mensajes_rotativos)
    session = tls_client.Session(client_identifier="chrome_120", random_tls_extension_order=True)
    payload = {"data": mensaje_a_enviar}

    timestamp = datetime.datetime.now().strftime('%H:%M:%S')
    # flush=True es vital para ver logs en Render
    print(f"[{timestamp}] Intentando enviar: {mensaje_a_enviar[:40]}...", flush=True) 

    try:
        response = session.post(URL, headers=HEADERS, json=payload)
        
        if response.status_code in [200, 201]:
            print("   -> Éxito ✅", flush=True)
            notificar_telegram(f"✅ <b>Mensaje Enviado</b>\nStatus: {response.status_code}\nMsg: <i>{mensaje_a_enviar[:30]}...</i>")
        else:
            print(f"   -> Fallo ❌: {response.text}", flush=True)
            notificar_telegram(f"❌ <b>Error Enviando</b>\nStatus: {response.status_code}\nResponse: {response.text}")
            
    except Exception as e:
        fail_msg = f"⚠️ <b>Excepción Crítica</b>\n{str(e)}"
        print(fail_msg, flush=True)
        notificar_telegram(fail_msg)

# --- BUCLE PRINCIPAL ---
def run_bot_logic():
    print("🤖 Hilo del Bot iniciado...", flush=True)
    time.sleep(10) # Espera a que Flask arranque
    
    enviar_shout() # Primer envío

    while True:
        segundos_min = MIN_MINUTOS * 60
        segundos_max = MAX_MINUTOS * 60
        tiempo_espera = random.uniform(segundos_min, segundos_max)
        
        proximo = datetime.datetime.now() + datetime.timedelta(seconds=tiempo_espera)
        
        print(f"⏳ Esperando {tiempo_espera/60:.2f} mins. Próximo: {proximo.strftime('%H:%M:%S')}", flush=True)
        
        time.sleep(tiempo_espera)
        enviar_shout()

# --- ARRANQUE CORREGIDO PARA RENDER ---
# Esto se ejecuta al importar el archivo (Gunicorn lo hace al arrancar)
try:
    # Verificamos si ya existe el hilo para no duplicarlo
    if not any(t.name == "BotThread" for t in threading.enumerate()):
        hilo_bot = threading.Thread(target=run_bot_logic, name="BotThread")
        hilo_bot.daemon = True
        hilo_bot.start()
except Exception as e:
    print(f"Error al iniciar hilo: {e}", flush=True)

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
