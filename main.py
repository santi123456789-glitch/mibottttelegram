import telebot
import requests
import os

BOT_TOKEN = os.getenv("BOT_TOKEN", "7401135193:AAFZTHeF_YcU4ROosBoNHgC6pOmoipU9QSc")
API_KEY = os.getenv("API_KEY", "C98M0NCRAD0K1BT2.")
SYMBOL = "EUR/USD"

bot = telebot.TeleBot(BOT_TOKEN)

# Guardamos el último precio
last_price = None

def get_price():
    url = f"https://www.alphavantage.co/query?function=CURRENCY_EXCHANGE_RATE&from_currency=EUR&to_currency=USD&apikey={API_KEY}"
    response = requests.get(url)
    data = response.json()

    try:
        price = float(data["Realtime Currency Exchange Rate"]["5. Exchange Rate"])
        return price
    except Exception as e:
        print("Error al obtener precio:", e)
        return None

@bot.message_handler(commands=['start'])
def send_welcome(message):
    markup = telebot.types.InlineKeyboardMarkup()
    button = telebot.types.InlineKeyboardButton("EUR/USD 💶💵", callback_data="check_price")
    markup.add(button)
    bot.send_message(message.chat.id, "📊 Elegí una moneda para ver la señal:", reply_markup=markup)

@bot.callback_query_handler(func=lambda call: call.data == "check_price")
def handle_price_check(call):
    global last_price
    current_price = get_price()

    if current_price is None:
        bot.send_message(call.message.chat.id, "❌ Error al obtener el precio.")
        return

    # Mostrar el botón de nuevo cada vez
    markup = telebot.types.InlineKeyboardMarkup()
    button = telebot.types.InlineKeyboardButton("EUR/USD 💶💵", callback_data="check_price")
    markup.add(button)

    if last_price is None:
        last_price = current_price
        msg = f"💱 Precio actual EUR/USD: {current_price:.5f}\n(Toca de nuevo para ver si sube o baja)"
    else:
        if current_price > last_price:
            msg = f"📈 El precio SUBIÓ: {current_price:.5f} 🔼"
        elif current_price < last_price:
            msg = f"📉 El precio BAJÓ: {current_price:.5f} 🔽"
        else:
            msg = f"➡ El precio se MANTUVO: {current_price:.5f}"

        last_price = current_price

    bot.send_message(call.message.chat.id, msg, reply_markup=markup)

print("✅ Bot corriendo...")
bot.infinity_polling()

