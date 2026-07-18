import os
import subprocess
import threading
import telebot
import requests
import html
from flask import Flask
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton

app = Flask(__name__)

@app.route("/")
def home():
    return "🌐 SYSTEM STATUS: OPERATIONAL. VEHICLE ENGINE ACTIVE."

# Configuration Matrix
BOT_TOKEN = os.getenv("BOT_TOKEN")
bot = telebot.TeleBot(BOT_TOKEN)
OWNER_ID = 6508791739
CHANNEL = "@tech_updates_india0763"

# Live Monitoring Alert Pipeline
def log_to_owner(log_text):
    try:
        bot.send_message(OWNER_ID, log_text, parse_mode='HTML', disable_web_page_preview=True)
    except Exception:
        pass

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
    user_id = message.from_user.id
    username = message.from_user.username or "N/A"
    
    # Send metrics stream update to owner
    log_to_owner(f"🛰️ <b>[SYSTEM ACCESS]:</b>\n👤 User: @{html.escape(username)}\n🆔 ID: <code>{user_id}</code>")

    if user_id == OWNER_ID:
        bot.reply_to(
            message,
            "🧬 <b>[ACCESS GRANTED • MASTER ADMIN]</b> 🧬\n━━━━━━━━━━━━━━━━━━━━━━━━━━\n\n"
            "🚗 <b>Vehicle Intelligence Core is Ready.</b>\n"
            "Execute query via command sequence: <code>/v [VEHICLE_NUMBER]</code>\n\n"
            "📥 <i>Standing by for data array input...</i>",
            parse_mode="HTML"
        )
    elif is_joined(user_id):
        bot.reply_to(
            message,
            "⚡ <b>VEHICLE COGNITIVE MATRIX ACTIVE</b> ⚡\n━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n\n"
            "Ready to fetch target data arrays from database systems.\n\n"
            "⚙️ <b>USAGE PATTERN:</b> <code>/v [VEHICLE_NUMBER]</code>\n"
            "👉 <i>Example:</i> <code>/v DL1CA1234</code>",
            parse_mode="HTML"
        )
    else:
        markup = InlineKeyboardMarkup()
        markup.add(InlineKeyboardButton("📢 Connect To Network Node", url="https://t.me/tech_updates_india0763"))
        
        bot.reply_to(
            message,
            "🔒 <b>ACCESS RESTRICTED • SECURITY GATEWAY</b>\n━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n\n"
            "To activate this vehicle lookup engine terminal, you must synchronize with our verification node.\n\n"
            "Please link up with the official network using the button below and re-initialize with /start.",
            reply_markup=markup,
            parse_mode="HTML"
        )

# 🚀 CORE UPGRADE: Handles ONLY text explicitly starting with the /v structure parameter
@bot.message_handler(func=lambda message: message.text.strip().startswith('/v '))
def vehicle_lookup(message):
    user_id = message.from_user.id
    username = message.from_user.username or "N/A"

    if not is_joined(user_id):
        markup = InlineKeyboardMarkup()
        markup.add(InlineKeyboardButton("📢 Connect To Network Node", url="https://t.me/tech_updates_india0763"))
        bot.reply_to(message, "❌ <b>Security Rejection:</b> Node registration missing from verified channel.", reply_markup=markup, parse_mode="HTML")
        return

    # Isolate extraction variable parameter from the text execution block cleanly
    vehicle = message.text.strip().split('/v ', 1)[1].strip().upper()

    if not vehicle:
        bot.reply_to(message, "⚠️ <b>Empty Query Matrix:</b> Please parse a valid license plate code format.\nUsage: <code>/v DL1CA1234</code>", parse_mode="HTML")
        return

    # Pipe real-time tracking metrics to the owner console terminal link
    log_to_owner(f"🔍 <b>[VEHICLE SCAN INITIATED]:</b>\n👤 Operator: @{html.escape(username)}\n🆔 ID: <code>{user_id}</code>\n🎯 Target Plate: <code>{html.escape(vehicle)}</code>")

    status_msg = bot.reply_to(message, f"📡 <b>[TUNNEL LAYER]:</b> Intercepting vehicle registry systems for <code>{vehicle}</code>...", parse_mode="HTML")
    url = f"http://vehicle-info-tnkq.onrender.com/fetch?vehicle={vehicle}"

    try:
        response = requests.get(url, timeout=20)
        data = response.json()

        if not data.get("success"):
            bot.edit_message_text("❌ <b>Registry Error:</b> Specified vehicle matrix not found inside national server cache.", message.chat.id, status_msg.message_id, parse_mode="HTML")
            return

        v = data.get("vehicle_data", {})
        r = v.get("rtoData", {})

        text = f"""
⚡ <b>VEHICLE INTEL REPORT SECURED</b> ⚡
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

🚘 <b>Vehicle Number:</b> <code>{v.get('regNo','N/A')}</code>
👤 <b>Registered Owner:</b> <code>{v.get('owner','N/A')}</code>
👨‍👦 <b>Father/Husband Name:</b> <code>{v.get('ownerFatherName','N/A')}</code>

🏭 <b>Manufacturer Unit:</b> {v.get('manufacturer','N/A')}
🚙 <b>Model Profile:</b> {v.get('vehicle','N/A')}
🔖 <b>Variant Spec:</b> {v.get('variant','N/A')}

⛽ <b>Fuel Subsystem:</b> {v.get('fuelType','N/A')}
🚐 <b>Vehicle Class Structure:</b> {v.get('vehicleClass','N/A')}
🚘 <b>Body Classification:</b> {v.get('vehicleType','N/A')}

🛠 <b>Engine Signature:</b> <code>{v.get('engine','N/A')}</code>
🆔 <b>Chassis Framework:</b> <code>{v.get('chassis','N/A')}</code>
⚙ <b>Displacement (CC):</b> {v.get('cubicCapacity','N/A')} CC
💺 <b>Seating Setup:</b> {v.get('seatCapacity','N/A')} Seats

📅 <b>Registration Date:</b> {v.get('regDate','N/A')}
🏭 <b>Manufacturing Era:</b> {v.get('manufacturerMonthYear','N/A')}

🏢 <b>Regional RTO Office:</b> {r.get('rtoName','N/A')}
📍 <b>RTO Terminal Code:</b> {r.get('rtoCode','N/A')}
🌍 <b>State Jurisdiction:</b> {r.get('statename','N/A')}
🏛 <b>Enforcing Authority:</b> {v.get('regAuthority','N/A')}

🏠 <b>Present Registered Address:</b>
<i>{v.get('presentAddress','N/A')}</i>

🏡 <b>Permanent Registered Address:</b>
<i>{v.get('permAddress','N/A')}</i>

🏦 <b>Financer Alliance:</b> {v.get('financerName','N/A')}

🛡 <b>Insurance Ledger Status:</b>
├ <b>Company:</b> {v.get('insuranceCompanyName','N/A')}
├ <b>Policy Index:</b> <code>{v.get('insurancePolicyNumber','N/A')}</code>
└ <b>Expiration Threshold:</b> {v.get('insuranceUpto','N/A')}

🌫 <b>PUCC Certificate No:</b> <code>{v.get('puccNumber','N/A')}</code>
📆 <b>PUCC Safe Threshold:</b> {v.get('puccValidUpto','N/A')}

📮 <b>Postal Pincode:</b> {v.get('pincode','N/A')}
📱 <b>Linked Cellular Line:</b> <code>{data.get('mobile_number','N/A')}</code>

📊 <b>Operational Status:</b> <b>{v.get('status','N/A')}</b>

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
👑 <b>NETWORK SYSTEM MASTERMIND:</b> @tomar_ji_99
"""
        bot.delete_message(chat_id=message.chat.id, message_id=status_msg.message_id)
        bot.reply_to(message, text, parse_mode="HTML")

    except Exception as e:
        bot.edit_message_text(f"⚠️ <b>Pipeline Runtime Fault:</b>\n<code>{html.escape(str(e))}</code>", message.chat.id, status_msg.message_id, parse_mode="HTML")

def run_bot():
    print("Tomar Ji Vehicle System Online Matrix Deploying...")
    bot.infinity_polling(skip_pending=True)

if __name__ == "__main__":
    # Start polling on a detached background daemon thread safely
    threading.Thread(target=run_bot, daemon=True).start()
    
    # Bind directly to Render's dynamic system port mappings environment
    app.run(
        host="0.0.0.0",
        port=int(os.environ.get("PORT", 10000))
    )
