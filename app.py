import os
import threading
import telebot
import requests
import html
from flask import Flask
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton

app = Flask(__name__)

@app.route("/")
def home():
    return "🌐 SYSTEM STATUS: OPERATIONAL. INTEL CORE ACTIVE."

# Configuration
BOT_TOKEN = os.getenv("BOT_TOKEN")
bot = telebot.TeleBot(BOT_TOKEN)
OWNER_ID = 6508791739
CHANNEL = "@tech_updates_india0763"
DEV_CREDIT = "@tomar_ji_99"

# Protected List (Direct match & Normalized match)
PROTECTED_NUMBERS = ["9926888306", "6508791739"]

def is_protected(input_str):
    clean = "".join(filter(str.isdigit, str(input_str)))
    for p in PROTECTED_NUMBERS:
        if clean.endswith(p):
            return True
    return False

def get_protected_warning():
    return (
        "⚠️ <b>[RESTRICTED ENTITY / SECURITY OVERRIDE]</b> ⚠️\n"
        "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n"
        "⛔ <b>ACCESS VIOLATION:</b> Target profile is protected by elite-level cyber security architecture.\n\n"
        "🛡️ <b>STATUS:</b> Premium / Top-Tier Ethical Hacker Node.\n"
        "🚫 Scanning or intercepting this target is strictly prohibited by central protocols.\n"
        "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    )

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

# Clean command parser to handle group mentions like /num@BotUsername
def extract_param(text, command_prefix):
    parts = text.strip().split(maxsplit=1)
    if len(parts) > 1:
        return parts[1].strip()
    return ""

@bot.message_handler(commands=['start'])
def start(message):
    user_id = message.from_user.id
    username = message.from_user.username or "N/A"
    chat_type = message.chat.type
    
    log_to_owner(f"🛰️ <b>[SYSTEM ACCESS - /start]:</b>\n👤 User: @{html.escape(username)}\n🆔 ID: <code>{user_id}</code>\n💬 Chat Type: <code>{chat_type}</code>")

    if not is_joined(user_id):
        markup = InlineKeyboardMarkup()
        markup.add(InlineKeyboardButton("📢 Connect To Network Node", url="https://t.me/tech_updates_india0763"))
        bot.reply_to(
            message,
            "🔒 <b>ACCESS RESTRICTED • SECURITY GATEWAY</b>\n━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n\n"
            "To activate this lookup engine terminal, you must synchronize with our verification node.\n\n"
            "Please link up with the official network using the button below and re-initialize with /start.",
            reply_markup=markup,
            parse_mode="HTML"
        )
        return

    bot.reply_to(
        message,
        "⚡ <b>INTELLIGENCE CORE MATRIX ACTIVE</b> ⚡\n━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n\n"
        "🛠️ <b>AVAILABLE COMMAND MODULES:</b>\n\n"
        "1️⃣ <b>Phone Data Search:</b>\n"
        "👉 <code>/num 9006640786</code>\n\n"
        "2️⃣ <b>Aadhaar Query Engine:</b>\n"
        "👉 <code>/aadhar [ID_QUERY]</code>\n\n"
        "3️⃣ <b>Network & Truecaller Analytics:</b>\n"
        "👉 <code>/true 9973700987</code>\n\n"
        "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n"
        f"👑 <b>CORE DEVELOPER:</b> {DEV_CREDIT}",
        parse_mode="HTML"
    )

# 1. /num Command
@bot.message_handler(commands=['num'])
def num_lookup(message):
    user_id = message.from_user.id
    username = message.from_user.username or "N/A"

    if not is_joined(user_id):
        markup = InlineKeyboardMarkup()
        markup.add(InlineKeyboardButton("📢 Connect To Network Node", url="https://t.me/tech_updates_india0763"))
        bot.reply_to(message, "❌ <b>Security Rejection:</b> Node registration missing.", reply_markup=markup, parse_mode="HTML")
        return

    target = extract_param(message.text, "/num").replace(" ", "")
    if not target:
        bot.reply_to(message, "⚠️ <b>Usage:</b> <code>/num 9006640786</code>", parse_mode="HTML")
        return

    log_to_owner(f"🔍 <b>[NUM SCAN]:</b>\n👤 @{html.escape(username)} | <code>{user_id}</code>\n🎯 Target: <code>{html.escape(target)}</code>\n📍 Chat: <code>{message.chat.type}</code>")

    if is_protected(target):
        bot.reply_to(message, get_protected_warning(), parse_mode="HTML")
        return

    status_msg = bot.reply_to(message, f"📡 <b>[QUERYING SYSTEM]:</b> Checking records for <code>{target}</code>...", parse_mode="HTML")
    url = f"https://x-trace-demo-number-full-info.vercel.app/apis/num_info_v1?key=@x_TRACEOWNER&num={target}"

    try:
        response = requests.get(url, timeout=20)
        data = response.json()

        if not data.get("success"):
            bot.edit_message_text("❌ <b>Error:</b> Record not found.", message.chat.id, status_msg.message_id, parse_mode="HTML")
            return

        total_records = data.get("total", 0)
        results = data.get("results", {})

        report = [
            "⚡ <b>NUMBER INTEL REPORT</b> ⚡",
            "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━",
            f"🎯 <b>Target:</b> <code>{html.escape(str(target))}</code>",
            f"📊 <b>Total Records:</b> <b>{total_records}</b>",
            "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
        ]

        if isinstance(results, dict):
            for key, val in results.items():
                if isinstance(val, dict):
                    name = val.get("name") or "N/A"
                    fname = val.get("fname") or "N/A"
                    mobile = val.get("mobile") or "N/A"
                    alt_mobile = val.get("alt") or "N/A"
                    circle = val.get("circle") or "N/A"
                    address = val.get("address") or "N/A"

                    report.append(
                        f"\n🔹 <b>RECORD #{int(key)+1 if key.isdigit() else key}</b>\n"
                        f"👤 <b>Name:</b> {html.escape(str(name))}\n"
                        f"👨‍👦 <b>Father:</b> {html.escape(str(fname))}\n"
                        f"📱 <b>Mobile:</b> <code>{html.escape(str(mobile))}</code>\n"
                        f"📞 <b>Alt:</b> <code>{html.escape(str(alt_mobile))}</code>\n"
                        f"🌐 <b>Circle:</b> {html.escape(str(circle))}\n"
                        f"📍 <b>Address:</b> <code>{html.escape(str(address))}</code>\n"
                    )

        report.append("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
        report.append(f"👑 <b>SYSTEM DEVELOPER:</b> {DEV_CREDIT}")

        bot.delete_message(chat_id=message.chat.id, message_id=status_msg.message_id)
        bot.reply_to(message, "\n".join(report), parse_mode="HTML")

    except Exception as e:
        bot.edit_message_text(f"⚠️ <b>Pipeline Fault:</b> <code>{html.escape(str(e))}</code>", message.chat.id, status_msg.message_id, parse_mode="HTML")

# 2. /aadhar Command
@bot.message_handler(commands=['aadhar'])
def aadhar_lookup(message):
    user_id = message.from_user.id
    username = message.from_user.username or "N/A"

    if not is_joined(user_id):
        markup = InlineKeyboardMarkup()
        markup.add(InlineKeyboardButton("📢 Connect To Network Node", url="https://t.me/tech_updates_india0763"))
        bot.reply_to(message, "❌ <b>Security Rejection:</b> Node registration missing.", reply_markup=markup, parse_mode="HTML")
        return

    target = extract_param(message.text, "/aadhar").replace(" ", "")
    if not target:
        bot.reply_to(message, "⚠️ <b>Usage:</b> <code>/aadhar [ID_QUERY]</code>", parse_mode="HTML")
        return

    log_to_owner(f"🔍 <b>[AADHAAR SCAN]:</b>\n👤 @{html.escape(username)} | <code>{user_id}</code>\n🎯 Target: <code>[Aadhaar Redacted]</code>\n📍 Chat: <code>{message.chat.type}</code>")

    if is_protected(target):
        bot.reply_to(message, get_protected_warning(), parse_mode="HTML")
        return

    status_msg = bot.reply_to(message, "📡 <b>[TUNNEL LAYER]:</b> Intercepting records...", parse_mode="HTML")
    url = f"https://x-trace-demo-aadhar-info-api.vercel.app/api?key=demo&aadhaar={target}"

    try:
        response = requests.get(url, timeout=20)
        res_data = response.json()

        data_list = res_data.get("response", {}).get("data", [])
        if not data_list:
            bot.edit_message_text("❌ <b>Error:</b> No entries mapped to this query.", message.chat.id, status_msg.message_id, parse_mode="HTML")
            return

        report = [
            "⚡ <b>AADHAAR REGISTRY REPORT</b> ⚡",
            "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━",
            "🎯 <b>Target ID:</b> <code>[Aadhaar Redacted]</code>",
            f"📊 <b>Total Records Mapped:</b> <b>{len(data_list)}</b>",
            "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
        ]

        for idx, item in enumerate(data_list, start=1):
            name = item.get("name") or "N/A"
            fname = item.get("fname") or "N/A"
            num = item.get("num") or "N/A"
            alt = item.get("alt") or "N/A"
            circle = item.get("circle") or "N/A"
            email = item.get("email") or "N/A"
            address = item.get("address") or "N/A"

            report.append(
                f"\n🔹 <b>ENTRY #{idx}</b>\n"
                f"👤 <b>Name:</b> {html.escape(str(name))}\n"
                f"👨‍👦 <b>Father:</b> {html.escape(str(fname))}\n"
                f"📱 <b>Phone:</b> <code>{html.escape(str(num))}</code>\n"
                f"📞 <b>Alt:</b> <code>{html.escape(str(alt))}</code>\n"
                f"📧 <b>Email:</b> {html.escape(str(email))}\n"
                f"🌐 <b>Circle:</b> {html.escape(str(circle))}\n"
                f"📍 <b>Address:</b> <code>{html.escape(str(address))}</code>\n"
            )

        report.append("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
        report.append(f"👑 <b>SYSTEM DEVELOPER:</b> {DEV_CREDIT}")

        bot.delete_message(chat_id=message.chat.id, message_id=status_msg.message_id)
        bot.reply_to(message, "\n".join(report), parse_mode="HTML")

    except Exception as e:
        bot.edit_message_text(f"⚠️ <b>Pipeline Fault:</b> <code>{html.escape(str(e))}</code>", message.chat.id, status_msg.message_id, parse_mode="HTML")

# 3. /true Command
@bot.message_handler(commands=['true'])
def true_lookup(message):
    user_id = message.from_user.id
    username = message.from_user.username or "N/A"

    if not is_joined(user_id):
        markup = InlineKeyboardMarkup()
        markup.add(InlineKeyboardButton("📢 Connect To Network Node", url="https://t.me/tech_updates_india0763"))
        bot.reply_to(message, "❌ <b>Security Rejection:</b> Node registration missing.", reply_markup=markup, parse_mode="HTML")
        return

    target = extract_param(message.text, "/true").replace(" ", "")
    if not target:
        bot.reply_to(message, "⚠️ <b>Usage:</b> <code>/true 9973700987</code>", parse_mode="HTML")
        return

    log_to_owner(f"🔍 <b>[TRUE SCAN]:</b>\n👤 @{html.escape(username)} | <code>{user_id}</code>\n🎯 Target: <code>{html.escape(target)}</code>\n📍 Chat: <code>{message.chat.type}</code>")

    if is_protected(target):
        bot.reply_to(message, get_protected_warning(), parse_mode="HTML")
        return

    status_msg = bot.reply_to(message, f"📡 <b>[TUNNEL LAYER]:</b> Analyzing network node for <code>{target}</code>...", parse_mode="HTML")
    url = f"https://x-trace-demo-truecaller-info-api.vercel.app/api.php?service=info-api&key=Demo&number={target}"

    try:
        response = requests.get(url, timeout=20)
        res = response.json()

        if not res.get("success"):
            bot.edit_message_text("❌ <b>Error:</b> Information could not be retrieved.", message.chat.id, status_msg.message_id, parse_mode="HTML")
            return

        data = res.get("data", {})

        report = (
            "⚡ <b>NETWORK & TELECOM INTEL</b> ⚡\n"
            "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n"
            f"📱 <b>Number:</b> <code>{html.escape(str(data.get('Number', target)))}</code>\n"
            f"👤 <b>Owner Name:</b> {html.escape(str(data.get('Owner Name', 'N/A')))}\n"
            f"📍 <b>Hometown:</b> {html.escape(str(data.get('Hometown', 'N/A')))}\n"
            f"🏢 <b>SIM Operator:</b> {html.escape(str(data.get('SIM Card', 'N/A')))}\n"
            f"📶 <b>Connection:</b> {html.escape(str(data.get('Connection', 'N/A')))}\n"
            f"🌐 <b>State/Circle:</b> {html.escape(str(data.get('Mobile State', 'N/A')))}\n"
            f"🏙️ <b>Reference City:</b> {html.escape(str(data.get('Reference City', 'N/A')))}\n"
            f"🗺️ <b>Mobile Locations:</b> {html.escape(str(data.get('Mobile Locations', 'N/A')))}\n"
            f"📡 <b>Tower Locations:</b> {html.escape(str(data.get('Tower Locations', 'N/A')))}\n"
            f"🚨 <b>Complaints:</b> {html.escape(str(data.get('Complaints', '0')))}\n"
            "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n"
            f"👑 <b>SYSTEM DEVELOPER:</b> {DEV_CREDIT}"
        )

        bot.delete_message(chat_id=message.chat.id, message_id=status_msg.message_id)
        bot.reply_to(message, report, parse_mode="HTML")

    except Exception as e:
        bot.edit_message_text(f"⚠️ <b>Pipeline Fault:</b> <code>{html.escape(str(e))}</code>", message.chat.id, status_msg.message_id, parse_mode="HTML")

# 4. Silent Message Tracker (Only logs to owner, never sends error messages in groups)
@bot.message_handler(func=lambda message: True)
def track_all_other_messages(message):
    user_id = message.from_user.id
    username = message.from_user.username or "N/A"
    text = message.text or "[Non-Text / Media]"
    chat_type = message.chat.type

    # Owner ID par silent log bhejta rahega
    log_to_owner(
        f"📩 <b>[MESSAGE LOG - {chat_type.upper()}]:</b>\n"
        f"👤 User: @{html.escape(username)}\n"
        f"🆔 ID: <code>{user_id}</code>\n"
        f"💬 Message: <code>{html.escape(text)}</code>"
    )

    # Private DM me invalid input alert dega, groups me bilkul shant rahega
    if chat_type == 'private':
        bot.reply_to(message, "⚠️ <b>Invalid Command.</b>\nPlease use /start to see available commands.", parse_mode="HTML")

def run_bot():
    print("Intelligence Matrix Online...")
    bot.infinity_polling(skip_pending=True)

if __name__ == "__main__":
    threading.Thread(target=run_bot, daemon=True).start()
    app.run(
        host="0.0.0.0",
        port=int(os.environ.get("PORT", 10000))
        )
        
