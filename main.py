import tls_client
import time
import random
import datetime
from itertools import cycle # Importamos esto para hacer la rotación

# --- CONFIGURACIÓN DE TIEMPO ---
MIN_MINUTOS = 15
MAX_MINUTOS = 20

# --- TUS MENSAJES (Se enviarán en este orden y luego se repetirán) ---
LISTA_MENSAJES = [
    "🚀 **ONLY $75 USD – LIMITED TIME ➤** Config Cloud + OpenBullet Guide (113 Pages) | Web & App Configs step-by-step from scratch 🔥 **➜** https://t.me/myConfigCloud",
    
    "🔥🦠 $50 USD LIFETIME! ➤ 140+ Auto-Updating Configs for Openbullet & Silverbullet ➤ Accepting Custom Requests - https://t.me/myConfigCloud",
    
    "⚡ **START NOW – PAY LATER ➤** Cracking E-Book + Config Cloud | **Learn Web & App configs from 0, sell your own work, get 155+ auto-updated configs** https://t.me/myConfigCloud"
]

# Preparamos el rotador de mensajes
mensajes_rotativos = cycle(LISTA_MENSAJES)

# Configuración del Request
URL = "https://chat2.patched.to/message/marketplace"

headers = {
    "accept": "application/json, text/plain, */*",
    "accept-language": "es-AR,es;q=0.9,en-US;q=0.8,en;q=0.7,es-419;q=0.6",
    "authorization": "eyJ1aWQiOjM0NjMyLCJhdmF0YXIiOiIuXC91cGxvYWRzXC9hdmF0YXJzXC9hdmF0YXJfMzQ2MzIucG5nP2RhdGVsaW5lPTE3NjY0MjQwMzkiLCJiYW5uZXIiOiIiLCJ0aXRsZSI6Ilx1ZDgzZVx1ZGM4MiBodHRwczpcL1wvdmlydXNudG8uY29tIFx1ZDgzZVx1ZGM4MCIsInVzZXJuYW1lIjoiVmlydXNOVE8iLCJncm91cCI6eyJpZCI6MiwiaW1hZ2UiOiJodHRwczpcL1wvY2RuLnBhdGNoZWQuc2hcL3JhbmtzXC9tZW1iZXIucG5nIn0sImljb24iOiJcL2ltYWdlc1wvYXNzZXRzXC9pdGVtc1wvZmxhZ3NcL2FyZ2VudGluYS5wbmciLCJzb2NpYWwiOnsiZGlzY29yZCI6Indob2lzbWF0dGhldyIsInRlbGVncmFtIjoiQHdob2lzX3R5bGVyIn0sIm5hbWVzdHlsZSI6IjxzcGFuIHN0eWxlPVwiY29sb3I6IHJnYmEoMjU1LDI1NSwyNTUsMC45MCk7XCI-PHN0cm9uZz5WaXJ1c05UTzxcL3N0cm9uZz48XC9zcGFuPiIsInN0YXRpc3RpY3MiOnsicG9zdCI6MTA4MSwidGhyZWFkIjozMn0sImV4cGlyZWQiOjE3Njg4OTM0Mjl9.0gj1YJ7sy2g.FHyveG5opR-y5pCYxEQfFH3HhQLeT5DMhlbsNfiqWag4A5nEEtV62x-uSmKJH-lcp9q7q0DvW5qFQLSqVwYuDA",
    "content-type": "application/json",
    "origin": "https://patched.to",
    "priority": "u=1, i",
    "referer": "https://patched.to/",
    "sec-ch-ua": '"Not(A:Brand";v="8", "Chromium";v="144", "Google Chrome";v="144"',
    "sec-ch-ua-mobile": "?0",
    "sec-ch-ua-platform": '"Windows"',
    "sec-fetch-dest": "empty",
    "sec-fetch-mode": "cors",
    "sec-fetch-site": "same-site",
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/144.0.0.0 Safari/537.36",
    "x-api-key": "28c58f7376e44cdfb0f012039a82d13f"
}

def enviar_shout():
    # Obtenemos el SIGUIENTE mensaje de la lista rotativa
    mensaje_a_enviar = next(mensajes_rotativos)
    
    session = tls_client.Session(
        client_identifier="chrome_120",
        random_tls_extension_order=True
    )
    
    payload = {"data": mensaje_a_enviar}

    try:
        print(f"[{datetime.datetime.now().strftime('%H:%M:%S')}] Enviando mensaje...")
        # Imprimimos los primeros 50 caracteres para que sepas cual se mandó
        print(f"   📝 Contenido: {mensaje_a_enviar[:50]}...") 
        
        response = session.post(URL, headers=headers, json=payload)
        
        if response.status_code in [200, 201]:
            print(f"   ✅ Enviado correctamente. (Status: {response.status_code})")
        else:
            print(f"   ❌ Error. Status: {response.status_code} | Resp: {response.text}")
            
    except Exception as e:
        print(f"   ⚠️ Excepción: {e}")

# Bucle principal
print(f"🤖 Bot Multimensaje iniciado. Intervalo: {MIN_MINUTOS} - {MAX_MINUTOS} min.")
enviar_shout() # Envía el mensaje 1 inmediatamente

while True:
    segundos_min = MIN_MINUTOS * 60
    segundos_max = MAX_MINUTOS * 60
    
    tiempo_espera = random.uniform(segundos_min, segundos_max)
    proximo_envio = datetime.datetime.now() + datetime.timedelta(seconds=tiempo_espera)
    
    print(f"⏳ Esperando {tiempo_espera:.2f} segundos.")
    print(f"📅 Próximo mensaje: {proximo_envio.strftime('%H:%M:%S')}")
    print("-" * 40)
    
    time.sleep(tiempo_espera)
    enviar_shout()
