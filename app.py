import tls_client
import time
import random
import datetime
import threading
import requests
import os
import sys
from flask import Flask
from itertools import cycle

# --- TUS DATOS ---
TELEGRAM_BOT_TOKEN = "8512201629:AAFYKnKttqURljq28VB3yjrdpK4HwFsSf2I" 
TELEGRAM_CHAT_ID = "-5172904911" 

# --- CONFIGURACIÓN ---
MIN_MINUTOS = 31
MAX_MINUTOS = 36
MAX_ERRORES_CONSECUTIVOS = 5

URL = "https://chat2.patched.to/message/marketplace"

# --- TU TOKEN ---
CURRENT_TOKEN = "eyJ1aWQiOjM0NjMyLCJhdmF0YXIiOiIuXC91cGxvYWRzXC9hdmF0YXJzXC9hdmF0YXJfMzQ2MzIucG5nP2RhdGVsaW5lPTE3NjY0MjQwMzkiLCJiYW5uZXIiOiIiLCJ0aXRsZSI6Ilx1ZDgzZVx1ZGM4MiBodHRwczpcL1wvdmlydXNudG8uY29tIFx1ZDgzZVx1ZGM4MCIsInVzZXJuYW1lIjoiVmlydXNOVE8iLCJncm91cCI6eyJpZCI6MiwiaW1hZ2UiOiJodHRwczpcL1wvY2RuLnBhdGNoZWQuc2hcL3JhbmtzXC9tZW1iZXIucG5nIn0sImljb24iOiJcL2ltYWdlc1wvYXNzZXRzXC9pdGVtc1wvZmxhZ3NcL2FyZ2VudGluYS5wbmciLCJzb2NpYWwiOnsiZGlzY29yZCI6Indob2lzbWF0dGhldyIsInRlbGVncmFtIjoiQHdob2lzX3R5bGVyIn0sIm5hbWVzdHlsZSI6IjxzcGFuIHN0eWxlPVwiY29sb3I6IHJnYmEoMjU1LDI1NSwyNTUsMC45MCk7XCI-PHN0cm9uZz5WaXJ1c05UTzxcL3N0cm9uZz48XC9zcGFuPiIsInN0YXRpc3RpY3MiOnsicG9zdCI6MTA5NSwidGhyZWFkIjozMn0sImV4cGlyZWQiOjE3NjkyODUxNzl9.skgFuaV3PFc.LQpzZ5YnOmQ7lrw9rm1en5G73waoHOEiiVnfQ92dwJl1qXWoB_nz0NXjHUdFHE-Mu4oWx4Rcx9uzxtFmK2q1Ag"

LISTA_MENSAJES = [
    "🚀 **ONLY $75 USD – LIMITED TIME ➤** Config Cloud + OpenBullet Guide (113 Pages) | Web & App Configs step-by-step from scratch 🔥 **➜** https://t.me/myConfigCloud",
    "🔥🦠 $50 USD LIFETIME! ➤ 140+ Auto-Updating Configs for Openbullet & Silverbullet ➤ Accepting Custom Requests - https://t.me/myConfigCloud",
    "⚡ **START NOW – PAY LATER ➤** Cracking E-Book + Config Cloud | **Learn Web & App configs from 0, sell your own work, get 155+ auto-updated configs** https://t.me/myConfigCloud"
]

mensajes_rotativos = cycle(LISTA_MENSAJES)

# ==========================================
#  SERVIDOR FLASK (Requerido para Render)
# ==========================================
app = Flask(__name__) # <--- ESTO ES LO QUE FALTABA

@app.route('/')
def home():
    return "Bot Activo - UptimeRobot OK"

# ==========================================
#  LÓGICA DEL BOT
# ==========================================

def notificar_telegram(mensaje):
    try:
        url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
        payload = { "chat_id": TELEGRAM_CHAT_ID, "text": mensaje, "parse_mode": "HTML" }
        requests.post(url, json=payload, timeout=5)
    except:
        pass

def obtener_headers(token):
    return {
        "accept": "application/json, text/plain, */*",
        "accept-language": "es-AR,es;q=0.9,en-US;q=0.8,en;q=0.7",
        "authorization": token,
        "content-type": "application/json",
        "origin": "https://patched.to",
        "referer": "https://patched.to/",
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
        "x-api-key": "28c58f7376e44cdfb0f012039a82d13f"
    }

def run_bot_logic():
    global CURRENT_TOKEN
    print("🤖 Hilo del Bot iniciado en Render...", flush=True)
    time.sleep(10) # Espera a que Flask arranque
    
    errores_consecutivos = 0
    session = tls_client.Session(client_identifier="chrome_120", random_tls_extension_order=True)
    
    # Intento inicial
    try:
        first_msg = next(mensajes_rotativos)
        # Nota: En Render probablemente necesitarás PROXY aquí abajo
        # session.proxies = {"http": "...", "https": "..."}
        
        print(f"Intento inicial: {first_msg[:30]}...", flush=True)
        session.post(URL, headers=obtener_headers(CURRENT_TOKEN), json={"data": first_msg})
    except:
        pass

    while True:
        minutos = random.uniform(MIN_MINUTOS, MAX_MINUTOS)
        segundos_espera = minutos * 60
        proximo = datetime.datetime.now() + datetime.timedelta(seconds=segundos_espera)
        
        print(f"⏳ Esperando {minutos:.2f} mins. Próximo: {proximo.strftime('%H:%M:%S')}", flush=True)
        time.sleep(segundos_espera)

        # Chequeo de seguridad
        if errores_consecutivos >= MAX_ERRORES_CONSECUTIVOS:
            print("⛔ APAGADO DE EMERGENCIA", flush=True)
            notificar_telegram("⛔ Bot apagado en Render por exceso de errores.")
            sys.exit()

        mensaje_actual = next(mensajes_rotativos)
        print(f"Procesando envío...", flush=True)

        try:
            payload = {"data": mensaje_actual}
            response = session.post(URL, headers=obtener_headers(CURRENT_TOKEN), json=payload)
            
            if response.status_code in [200, 201]:
                print(f"   ✅ Enviado OK", flush=True)
                errores_consecutivos = 0
                notificar_telegram(f"✅ Msg Enviado. Status: {response.status_code}")

            elif response.status_code == 401:
                print("   ❌ TOKEN CADUCADO (401)", flush=True)
                notificar_telegram("⚠️ <b>Token Vencido en Render</b>. Actualiza la variable o el código.")
                # En Render no podemos usar input(), así que esperamos mucho tiempo
                errores_consecutivos += 1
                time.sleep(300) 

            else:
                errores_consecutivos += 1
                print(f"   ⚠️ Error {response.status_code}", flush=True)
                
        except Exception as e:
            errores_consecutivos += 1
            print(f"   ⚠️ Excepción: {e}", flush=True)

# ==========================================
#  ARRANQUE (IMPORTANTE PARA RENDER)
# ==========================================

# Iniciamos el bot en segundo plano al importar
try:
    if not any(t.name == "BotThread" for t in threading.enumerate()):
        hilo_bot = threading.Thread(target=run_bot_logic, name="BotThread")
        hilo_bot.daemon = True
        hilo_bot.start()
except Exception as e:
    print(f"Error hilo: {e}")

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
