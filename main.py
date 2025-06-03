import time
import requests

TELEGRAM_TOKEN = "8024006886:AAHhfBX0zaxm02x17tJXBPt45zuwP-hraEM"
CHAT_ID = "7633225167"

def enviar_senal(mensaje):
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    data = {
        "chat_id": CHAT_ID,
        "text": mensaje
    }
    requests.post(url, data=data)

def obtener_senal():
    # Simulamos una señal real cada 5 segundos
    return "📈 Señal de ejemplo: Comprar EUR/USD"

def main():
    while True:
        senal = obtener_senal()
        enviar_senal(senal)
        time.sleep(5)

if __name__ == "__main__":
    main()
