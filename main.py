import telebot
import requests
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton

BOT_TOKEN = "8024006886:AAHhfBX0zaxm02x17tJXBPt45zuwP-hraEM"
API_KEY = "EHLLSMJU9HV03O6H"

bot = telebot.TeleBot(BOT_TOKEN)

# Guardar el precio anterior
previous_price = None

# Crear el teclado con el botón EUR/USD
def get_currency_markup():
    markup = InlineKeyboardMarkup()
    markup.add(InlineKeyboardButton("EUR/USD", callback_data="check_eurusd"))
    return markup

# Comando /start
@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id, "Elegí la moneda:", reply_markup=get_currency_markup())

# Al tocar el botón EUR/USD
@bot.callback_query_handler(func=lambda call: call.data == "check_eurusd")
def handle_currency_check(call):
    global previous_price

    url = f"https://www.alphavantage.co/query?function=CURRENCY_EXCHANGE_RATE&from_currency=EUR&to_currency=USD&apikey={API_KEY}"
    response = requests.get(url)
    data = response.json()

    try:
        current_price = float(data["Realtime Currency Exchange Rate"]["5. Exchange Rate"])
        message = f"💱 EUR/USD: {current_price:.5f}\n"

        if previous_price is not None:
            if current_price > previous_price:
                message += "📈 El precio SUBIÓ"
            elif current_price < previous_price:
                message += "📉 El precio BAJÓ"
            else:
                message += "➖ El precio NO CAMBIÓ"
        else:
            message += "Este es el primer valor consultado."

        previous_price = current_price
        bot.send_message(call.message.chat.id, message, reply_markup=get_currency_markup())

    except Exception as e:
        bot.send_message(call.message.chat.id, "⚠️ No se pudo obtener el precio.", reply_markup=get_currency_markup())

# Ejecutar el bot
bot.infinity_polling()

