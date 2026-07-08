import os
import threading
import telebot
import requests
from flask import Flask
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton

BOT_TOKEN = os.getenv("BOT_TOKEN")
bot = telebot.TeleBot(BOT_TOKEN)
OWNER_ID = 6508791739

app = Flask(__name__)

@app.route("/")
def home():
    return "Bot is running!"

CHANNEL = "@tech_updates_india0763"

def is_joined(user_id):
    if user_id == OWNER_ID:
        return True

    try:
        member = bot.get_chat_member(CHANNEL, user_id)
        return member.status in ["member", "administrator", "creator"]
    except:
        return False
@bot.message_handler(commands=['start'])
def start(message):
    if is_joined(message.from_user.id):
        bot.reply_to(
            message,
            "🚗 Vehicle Info Bot\n\nVehicle Number bhejo."
        )
    else:
        markup = InlineKeyboardMarkup()
        markup.add(
            InlineKeyboardButton(
                "📢 Join Channel",
                url="https://t.me/tech_updates_india0763"
            )
        )

        bot.reply_to(
            message,
            "❌ Bot use karne ke liye pehle hamara channel join karo.\n\nJoin karne ke baad phir /start bhejo.",
            reply_markup=markup
        )
@bot.message_handler(func=lambda m: True)
def vehicle_lookup(message):

    if not is_joined(message.from_user.id):
        markup = InlineKeyboardMarkup()
        markup.add(
            InlineKeyboardButton(
                "📢 Join Channel",
                url="https://t.me/tech_updates_india0763"
            )
        )

        bot.reply_to(
            message,
            "❌ Pehle channel join karein.",
            reply_markup=markup
        )
        return

    vehicle = message.text.strip().upper()

    url = f"http://vehicle-info-tnkq.onrender.com/fetch?vehicle={vehicle}"

    try:
        response = requests.get(url, timeout=20)
        data = response.json()

        if not data.get("success"):
            bot.reply_to(message, "❌ Vehicle Not Found.")
            return

        v = data.get("vehicle_data", {})
        r = v.get("rtoData", {})

        text = f"""
🚗 <b>VEHICLE DETAILS</b>

🚘 <b>Vehicle No:</b> {v.get('regNo','N/A')}
👤 <b>Owner:</b> {v.get('owner','N/A')}
👨‍👦 <b>Father:</b> {v.get('ownerFatherName','N/A')}

🏭 <b>Manufacturer:</b> {v.get('manufacturer','N/A')}
🚙 <b>Model:</b> {v.get('vehicle','N/A')}
🔖 <b>Variant:</b> {v.get('variant','N/A')}

⛽ <b>Fuel:</b> {v.get('fuelType','N/A')}
🚐 <b>Vehicle Class:</b> {v.get('vehicleClass','N/A')}
🚘 <b>Vehicle Type:</b> {v.get('vehicleType','N/A')}

🛠 <b>Engine:</b> {v.get('engine','N/A')}
🆔 <b>Chassis:</b> {v.get('chassis','N/A')}
⚙ <b>CC:</b> {v.get('cubicCapacity','N/A')}
💺 <b>Seats:</b> {v.get('seatCapacity','N/A')}

📅 <b>Registration:</b> {v.get('regDate','N/A')}
🏭 <b>MFG:</b> {v.get('manufacturerMonthYear','N/A')}

🏢 <b>RTO:</b> {r.get('rtoName','N/A')}
📍 <b>RTO Code:</b> {r.get('rtoCode','N/A')}
🌍 <b>State:</b> {r.get('statename','N/A')}
🏛 <b>Authority:</b> {v.get('regAuthority','N/A')}

🏠 <b>Present Address:</b>
{v.get('presentAddress','N/A')}

🏡 <b>Permanent Address:</b>
{v.get('permAddress','N/A')}

🏦 <b>Financer:</b>
{v.get('financerName','N/A')}

🛡 <b>Insurance:</b>
Company: {v.get('insuranceCompanyName','N/A')}
Policy: {v.get('insurancePolicyNumber','N/A')}
Valid Till: {v.get('insuranceUpto','N/A')}

🌫 <b>PUCC No:</b> {v.get('puccNumber','N/A')}
📆 <b>PUCC Valid:</b> {v.get('puccValidUpto','N/A')}

📮 <b>Pincode:</b> {v.get('pincode','N/A')}
📱 <b>Mobile:</b> {data.get('mobile_number','N/A')}

📊 <b>Status:</b> {v.get('status','N/A')}

👨‍💻 <b>Developer:</b>
@tomar_ji_99
"""

        bot.reply_to(message, text, parse_mode="HTML")

    except Exception as e:
        bot.reply_to(message, f"❌ Error:\n{e}")

print("Bot Running...")
def run_bot():
    print("Bot Running...")
    bot.infinity_polling(skip_pending=True)

threading.Thread(target=run_bot).start()

app.run(
    host="0.0.0.0",
    port=int(os.environ.get("PORT", 10000))
)
