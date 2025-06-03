import os
import time
import telebot
import requests

BOT_TOKEN = os.getenv("TELEGRAM_TOKEN")
CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")
bot = telebot.TeleBot(BOT_TOKEN)

def obtener_senal_fake():
    # Simulación de una señal aleatoria (en producción, reemplazar con señales reales)
    import random
    return random.choice(["📈 Señal: BUY (Compra)", "📉 Señal: SELL (Venta)", "❌ No hay señal clara"])

@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id, "✅ Bot iniciado. Enviando señales cada 5 segundos...")
    while True:
        senal = obtener_senal_fake()
        bot.send_message(message.chat.id, senal)
        time.sleep(5)

bot.polling()