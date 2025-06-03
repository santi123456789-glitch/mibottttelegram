import requests
import time
import telebot
import os

# Variables del entorno desde Render
TOKEN = os.getenv("TELEGRAM_TOKEN")
CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")

bot = telebot.TeleBot(TOKEN)

last_price = None

def get_price():
    url = "https://api.binance.com/api/v3/ticker/price?symbol=BTCUSDT"
    data = requests.get(url).json()
    return float(data["price"])

@bot.message_handler(commands=["start"])
def start(message):
    bot.send_message(message.chat.id, "✅ Bot de señales iniciado con datos reales.")
    monitor_price()

def monitor_price():
    global last_price
    while True:
        try:
            current_price = get_price()
            if last_price is not None:
                if current_price > last_price:
                    bot.send_message(CHAT_ID, f"📈 Señal REAL: El precio subió a {current_price}")
                elif current_price < last_price:
                    bot.send_message(CHAT_ID, f"📉 Señal REAL: El precio bajó a {current_price}")
            last_price = current_price
            time.sleep(5)  # cada 5 segundos
        except Exception as e:
            print("Error:", e)
            time.sleep(5)

# Iniciar el bot
bot.polling()

