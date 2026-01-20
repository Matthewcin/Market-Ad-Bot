import tls_client
import time
import random
import datetime
import threading
import requests
import os
from flask import Flask
from itertools import cycle

# --- CONFIGURACIÓN TELEGRAM ---
# Pon aquí el token de tu bot (habla con @BotFather)
TELEGRAM_BOT_TOKEN = "8512201629:AAFYKnKttqURljq28VB3yjrdpK4HwFsSf2I" 
# Pon tu ID numérico (habla con @userinfobot)
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

# --- CONFIGURACIÓN DE HEADERS (Patched.to) ---
URL = "https://chat2.patched.to/message/marketplace"
HEADERS = {
    "accept": "application/json, text/plain, */*",
    "accept-language": "es-AR,es;q=0.9,en-US;q=0.8,en;q=0.7,es-419;q=0.6",
    # NOTA: Si el token caduca, deberás actualizarlo aquí o usar Variables de Entorno en Render
    "authorization": "eyJ1aWQiOjM0NjMyLCJhdmF0YXIiOiIuXC91cGxvYWRzXC9hdmF0YXJzXC9hdmF0YXJfMzQ2MzIucG5nP2RhdGVsaW5lPTE3NjY0MjQwMzkiLCJiYW5uZXIiOiIiLCJ0aXRsZSI6Ilx1ZDgzZVx1ZGM4MiBodHRwczpcL1wvdmlydXNudG8uY29tIFx1ZDgzZVx1ZGM4MCIsInVzZXJuYW1lIjoiVmlydXNOVE8iLCJncm91cCI6eyJpZCI6MiwiaW1hZ2UiOiJodHRwczpcL1wvY2RuLnBhdGNoZWQuc2hcL3JhbmtzXC9tZW1iZXIucG5nIn0sImljb24iOiJcL2ltYWdlc1wvYXNzZXRzXC9pdGVtc1wvZmxhZ3NcL2FyZ2VudGluYS5wbmciLCJzb2NpYWwiOnsiZGlzY29yZCI6Indob2lzbWF0dGhldyIsInRlbGVncmFtIjoiQHdob2lzX3R5bGVyIn0sIm5hbWVzdHlsZSI6IjxzcGFuIHN0eWxlPVwiY29sb3I6IHJnYmEoMjU1LDI1NSwyNTUsMC45MCk7XCI-PHN0cm9uZz5WaXJ1c05UTzxcL3N0cm9uZz48XC9zcGFuPiIsInN0YXRpc3RpY3MiOnsicG9zdCI6MTA4MSwidGhyZWFkIjozMn0sImV4cGlyZWQiOjE3Njg4OTM0Mjl9.0gj1YJ7sy2g.FHyveG5opR-y5pCYxEQfFH3HhQLeT5DMhlbsNfiqWag4A5nEEtV62x-uSmKJH-lcp9q7q0DvW5qFQLSqVwYuDA",
    "content-type": "application/json",
    "origin": "https://patched.to",
    "referer": "https://patched.to/",
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/144.0.0.0 Safari/537.36",
    "x-api-key": "28c58f7376e44cdfb0f012039a82d13f"
}

# --- SERVIDOR FLASK (Para UptimeRobot) ---
app = Flask(__name__)

@app.route('/')
def home():
    return "Bot de Shoutbox Activo y Corriendo 24/7"

# --- FUNCIONES DE UTILIDAD ---

def notificar_telegram(mensaje):
    """Envía logs a tu Telegram personal"""
    if TELEGRAM_BOT_TOKEN == "TU_TOKEN_DEL_BOT_AQUI":
        return # No configurado
    
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    payload = {
        "chat_id": TELEGRAM_CHAT_ID,
        "text": mensaje,
        "parse_mode": "HTML"
    }
    try:
        requests.post(url, json=payload)
    except Exception as e:
        print(f"Error contactando Telegram: {e}")

def enviar_shout():
    mensaje_a_enviar = next(mensajes_rotativos)
    session = tls_client.Session(client_identifier="chrome_120", random_tls_extension_order=True)
    payload = {"data": mensaje_a_enviar}

    # Log para Consola Render
    timestamp = datetime.datetime.now().strftime('%H:%M:%S')
    log_msg = f"[{timestamp}] Intentando enviar: {mensaje_a_enviar[:40]}..."
    print(log_msg) 

    try:
        response = session.post(URL, headers=HEADERS, json=payload)
        
        if response.status_code in [200, 201]:
            exito_msg = f"✅ <b>Mensaje Enviado</b>\nStatus: {response.status_code}\nMsg: <i>{mensaje_a_enviar[:30]}...</i>"
            print("   -> Éxito")
            notificar_telegram(exito_msg)
        else:
            error_msg = f"❌ <b>Error Enviando</b>\nStatus: {response.status_code}\nResponse: {response.text}"
            print(f"   -> Fallo: {response.text}")
            notificar_telegram(error_msg)
            
    except Exception as e:
        fail_msg = f"⚠️ <b>Excepción Crítica</b>\n{str(e)}"
        print(fail_msg)
        notificar_telegram(fail_msg)

# --- BUCLE PRINCIPAL (THREAD) ---
def run_bot_logic():
    print("🤖 Hilo del Bot iniciado...")
    # Pequeña pausa inicial para que arranque Flask primero
    time.sleep(10) 
    
    # Enviar primero al iniciar
    enviar_shout()

    while True:
        segundos_min = MIN_MINUTOS * 60
        segundos_max = MAX_MINUTOS * 60
        tiempo_espera = random.uniform(segundos_min, segundos_max)
        
        proximo = datetime.datetime.now() + datetime.timedelta(seconds=tiempo_espera)
        aviso_espera = f"⏳ Esperando {tiempo_espera/60:.2f} mins.\nPróximo: {proximo.strftime('%H:%M:%S')}"
        print(aviso_espera)
        
        time.sleep(tiempo_espera)
        enviar_shout()

# --- ARRANQUE ---
if __name__ == '__main__':
    # Iniciamos el bot en un hilo separado para no bloquear Flask
    hilo_bot = threading.Thread(target=run_bot_logic)
    hilo_bot.daemon = True # Se cierra si la app principal muere
    hilo_bot.start()
    
    # Iniciamos el servidor web (necesario para Render)
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
