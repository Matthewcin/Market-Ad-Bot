import tls_client
import time
import random
import datetime
import requests
import sys
from itertools import cycle

# --- TUS DATOS DE TELEGRAM ---
TELEGRAM_BOT_TOKEN = "8512201629:AAFYKnKttqURljq28VB3yjrdpK4HwFsSf2I" 
TELEGRAM_CHAT_ID = "-5172904911" 

# --- CONFIGURACIÓN ---
MIN_MINUTOS = 31
MAX_MINUTOS = 36
MAX_ERRORES_CONSECUTIVOS = 5  # Si falla 5 veces seguidas, se apaga

URL = "https://chat2.patched.to/message/marketplace"

# --- TU NUEVO TOKEN (Ya cargado) ---
CURRENT_TOKEN = "eyJ1aWQiOjM0NjMyLCJhdmF0YXIiOiIuXC91cGxvYWRzXC9hdmF0YXJzXC9hdmF0YXJfMzQ2MzIucG5nP2RhdGVsaW5lPTE3NjY0MjQwMzkiLCJiYW5uZXIiOiIiLCJ0aXRsZSI6Ilx1ZDgzZVx1ZGM4MiBodHRwczpcL1wvdmlydXNudG8uY29tIFx1ZDgzZVx1ZGM4MCIsInVzZXJuYW1lIjoiVmlydXNOVE8iLCJncm91cCI6eyJpZCI6MiwiaW1hZ2UiOiJodHRwczpcL1wvY2RuLnBhdGNoZWQuc2hcL3JhbmtzXC9tZW1iZXIucG5nIn0sImljb24iOiJcL2ltYWdlc1wvYXNzZXRzXC9pdGVtc1wvZmxhZ3NcL2FyZ2VudGluYS5wbmciLCJzb2NpYWwiOnsiZGlzY29yZCI6Indob2lzbWF0dGhldyIsInRlbGVncmFtIjoiQHdob2lzX3R5bGVyIn0sIm5hbWVzdHlsZSI6IjxzcGFuIHN0eWxlPVwiY29sb3I6IHJnYmEoMjU1LDI1NSwyNTUsMC45MCk7XCI-PHN0cm9uZz5WaXJ1c05UTzxcL3N0cm9uZz48XC9zcGFuPiIsInN0YXRpc3RpY3MiOnsicG9zdCI6MTA5NSwidGhyZWFkIjozMn0sImV4cGlyZWQiOjE3NjkwOTcyNjl9.J2iddIVWxzo.fCCJmrNh8a1bahKdAAW75uzE9xFchZ39ip9wgTChXeJ7gFUw3IqA7F9w6iH5coeUGhnzf906aw9qeXRGP2p7Cw"

# Mensajes a rotar
LISTA_MENSAJES = [
    "🚀 **ONLY $75 USD – LIMITED TIME ➤** Config Cloud + OpenBullet Guide (113 Pages) | Web & App Configs step-by-step from scratch 🔥 **➜** https://t.me/myConfigCloud",
    "🔥🦠 $50 USD LIFETIME! ➤ 140+ Auto-Updating Configs for Openbullet & Silverbullet ➤ Accepting Custom Requests - https://t.me/myConfigCloud",
    "⚡ **START NOW – PAY LATER ➤** Cracking E-Book + Config Cloud | **Learn Web & App configs from 0, sell your own work, get 155+ auto-updated configs** https://t.me/myConfigCloud"
]

mensajes_rotativos = cycle(LISTA_MENSAJES)

def notificar_telegram(mensaje):
    """Envía alertas a tu Telegram"""
    try:
        url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
        payload = { "chat_id": TELEGRAM_CHAT_ID, "text": mensaje, "parse_mode": "HTML" }
        requests.post(url, json=payload, timeout=5)
    except Exception as e:
        print(f"⚠️ No se pudo enviar notificación a Telegram: {e}")

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

def main():
    global CURRENT_TOKEN
    print("🛡️  BOT DE SEGURIDAD ACTIVADO - Shoutbox")
    print(f"   -> Modo Anti-Ban: ON (Máx {MAX_ERRORES_CONSECUTIVOS} errores)")
    print("-------------------------------------")
    
    errores_consecutivos = 0
    session = tls_client.Session(client_identifier="chrome_120", random_tls_extension_order=True)

    while True:
        # 1. Comprobación de seguridad
        if errores_consecutivos >= MAX_ERRORES_CONSECUTIVOS:
            msg_fail = f"⛔ <b>BOT APAGADO POR SEGURIDAD</b>\nSe detectaron {errores_consecutivos} errores seguidos. Se detuvo para evitar ban de IP."
            print("\n" + "!"*40)
            print("⛔ APAGADO DE EMERGENCIA: DEMASIADOS ERRORES")
            print("!"*40)
            notificar_telegram(msg_fail)
            input("Presiona ENTER para cerrar...")
            sys.exit()

        # 2. Preparar mensaje
        mensaje_actual = next(mensajes_rotativos)
        timestamp = datetime.datetime.now().strftime('%H:%M:%S')
        print(f"\n[{timestamp}] Procesando envío...")

        try:
            payload = {"data": mensaje_actual}
            response = session.post(URL, headers=obtener_headers(CURRENT_TOKEN), json=payload)
            
            # --- ESCENARIO 1: ÉXITO (200/201) ---
            if response.status_code in [200, 201]:
                print(f"   ✅ Mensaje enviado correctamente.")
                errores_consecutivos = 0 # Reseteamos contador de peligro
                
                # Tiempo de espera
                minutos = random.uniform(MIN_MINUTOS, MAX_MINUTOS)
                segundos_espera = minutos * 60
                proximo = datetime.datetime.now() + datetime.timedelta(seconds=segundos_espera)
                
                print(f"   ⏳ Durmiendo {minutos:.2f} mins. Próximo: {proximo.strftime('%H:%M:%S')}")
                time.sleep(segundos_espera)

            # --- ESCENARIO 2: TOKEN VENCIDO (401) ---
            elif response.status_code == 401:
                print("   ❌ TOKEN CADUCADO (401)")
                notificar_telegram(f"⚠️ <b>TOKEN CADUCADO</b>\nEl bot requiere un nuevo token. Esperando input manual en PC.")
                
                # Bucle infinito hasta que el usuario ponga token nuevo
                while True:
                    nueva_auth = input("\n🔄 TOKEN VENCIDO. Pega el nuevo 'authorization' aquí: ").strip()
                    if len(nueva_auth) > 50: # Validación básica
                        CURRENT_TOKEN = nueva_auth
                        errores_consecutivos = 0 # Reseteamos errores porque ya lo arregló el humano
                        print("   ✅ Token actualizado. Reanudando en 5 segundos...")
                        notificar_telegram("✅ <b>Token Actualizado</b>. El bot vuelve al trabajo.")
                        time.sleep(5)
                        break # Rompe el bucle de input y vuelve al envio
                    else:
                        print("   ⚠️ Token muy corto, parece inválido.")

            # --- ESCENARIO 3: OTROS ERRORES (Peligro de Ban) ---
            else:
                errores_consecutivos += 1
                print(f"   ⚠️ Error {response.status_code}. Respuesta: {response.text[:50]}...")
                print(f"   ⚠️ Advertencia {errores_consecutivos}/{MAX_ERRORES_CONSECUTIVOS}")
                
                # Espera corta antes de reintentar
                time.sleep(10)

        except Exception as e:
            errores_consecutivos += 1
            print(f"   ⚠️ Excepción Crítica: {e}")
            time.sleep(10)

if __name__ == "__main__":
    main()
