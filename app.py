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
    return "🌐 SYSTEM STATUS: ONLINE"

# Configuration
BOT_TOKEN = os.getenv("BOT_TOKEN")
bot = telebot.TeleBot(BOT_TOKEN, parse_mode=None)

OWNER_ID = 6508791739
CHANNEL = "@tech_updates_india0763"
GROUP = "@allioneplace"
YOUTUBE_URL = "https://www.youtube.com/@hackeronall"
DEV_CREDIT = "@tomar_ji_99"

# Protected List
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
        "🛡️ <b>STATUS:</b> Premium / Top-Tier Node.\n"
        "🚫 Scanning or intercepting this target is strictly prohibited by central protocols.\n"
        "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    )

def log_to_owner(log_text):
    try:
        bot.send_message(OWNER_ID, log_text, parse_mode='HTML', disable_web_page_preview=True)
    except Exception:
        pass

def is_joined(user_id):
    # Owner ke liye verification hamesha True rahegi
    if str(user_id) == str(OWNER_ID):
        return True
    try:
        # Check Channel
        ch_member = bot.get_chat_member(CHANNEL, user_id)
        if ch_member.status not in ["member", "administrator", "creator"]:
            return False
        
        # Check Group
        grp_member = bot.get_chat_member(GROUP, user_id)
        if grp_member.status not in ["member", "administrator", "creator"]:
            return False
            
        return True
    except Exception:
        # Bot agar group/channel me admin nahi hai toh user block na ho
        return True

def get_join_markup():
    markup = InlineKeyboardMarkup(row_width=1)
    markup.add(
        InlineKeyboardButton("📢 Join Official Channel", url="https://t.me/tech_updates_india0763"),
        InlineKeyboardButton("💬 Join Telegram Group", url="https://t.me/allioneplace"),
        InlineKeyboardButton("▶️ Subscribe YouTube Channel", url=YOUTUBE_URL)
    )
    return markup

def send_restriction_message(message):
    bot.reply_to(
        message,
        "🔒 <b>ACCESS RESTRICTED</b>\n\n"
        "Bot use karne ke liye hamare Channel, Group aur YouTube ko join/subscribe karein fir <b>/start</b> dabayein.",
        reply_markup=get_join_markup(),
        parse_mode="HTML"
    )

def extract_param(text):
    parts = text.strip().split(maxsplit=1)
    if len(parts) > 1:
        return parts[1].strip()
    return ""

# START COMMAND
@bot.message_handler(commands=['start'])
def start_cmd(message):
    user_id = message.from_user.id
    username = message.from_user.username or "N/A"
    
    if user_id != OWNER_ID:
        log_to_owner(f"🛰️ <b>[ACCESS]:</b> @{html.escape(username)} (<code>{user_id}</code>)")

    if not is_joined(user_id):
        send_restriction_message(message)
        return

    welcome_text = (
        "⚡ <b>INTELLIGENCE CORE MATRIX ACTIVE</b> ⚡\n"
        "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n\n"
        "🛠️ <b>COMMANDS:</b>\n\n"
        "1️⃣ <b>Phone Data Search:</b>\n"
        "👉 <code>/num 9006640786</code>\n\n"
        "2️⃣ <b>ID Query Engine:</b>\n"
        "👉 <code>/aadhar [ID_QUERY]</code>\n\n"
        "3️⃣ <b>Network & Truecaller Analytics:</b>\n"
        "👉 <code>/true 9973700987</code>\n\n"
        "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n"
        f"👑 <b>SYSTEM DEVELOPER:</b> {DEV_CREDIT}"
    )
    bot.reply_to(message, welcome_text, parse_mode="HTML")

# 1. /num Command
@bot.message_handler(commands=['num'])
def num_cmd(message):
    user_id = message.from_user.id
    username = message.from_user.username or "N/A"

    if not is_joined(user_id):
        send_restriction_message(message)
        return

    target = extract_param(message.text).replace(" ", "")
    if not target:
        bot.reply_to(message, "⚠️ <b>Usage:</b> <code>/num 9006640786</code>", parse_mode="HTML")
        return

    if user_id != OWNER_ID:
        log_to_owner(f"🔍 <b>[NUM SCAN]:</b> @{html.escape(username)} | <code>{html.escape(target)}</code>")

    if is_protected(target):
        bot.reply_to(message, get_protected_warning(), parse_mode="HTML")
        return

    status_msg = bot.reply_to(message, f"📡 Intercepting records for <code>{target}</code>...", parse_mode="HTML")
    url = f"https://x-trace-demo-number-full-info.vercel.app/apis/num_info_v1?key=@x_TRACEOWNER&num={target}"

    try:
        res = requests.get(url, timeout=20).json()
        if not res.get("success"):
            bot.edit_message_text("❌ <b>Error:</b> Record not found.", message.chat.id, status_msg.message_id, parse_mode="HTML")
            return

        report = [
            "⚡ <b>NUMBER INTEL REPORT</b> ⚡",
            "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━",
            f"🎯 <b>Target:</b> <code>{html.escape(str(target))}</code>",
            f"📊 <b>Total Records:</b> <b>{res.get('total', 0)}</b>",
            "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
        ]

        results = res.get("results", {})
        if isinstance(results, dict):
            for key, val in results.items():
                if isinstance(val, dict):
                    report.append(
                        f"\n🔹 <b>RECORD #{int(key)+1 if key.isdigit() else key}</b>\n"
                        f"👤 <b>Name:</b> {html.escape(str(val.get('name', 'N/A')))}\n"
                        f"👨‍👦 <b>Father:</b> {html.escape(str(val.get('fname', 'N/A')))}\n"
                        f"📱 <b>Mobile:</b> <code>{html.escape(str(val.get('mobile', 'N/A')))}</code>\n"
                        f"📞 <b>Alt:</b> <code>{html.escape(str(val.get('alt', 'N/A')))}</code>\n"
                        f"🌐 <b>Circle:</b> {html.escape(str(val.get('circle', 'N/A')))}\n"
                        f"📍 <b>Address:</b> <code>{html.escape(str(val.get('address', 'N/A')))}</code>\n"
                    )

        report.append("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
        report.append(f"👑 <b>SYSTEM DEVELOPER:</b> {DEV_CREDIT}")

        bot.delete_message(message.chat.id, status_msg.message_id)
        bot.reply_to(message, "\n".join(report), parse_mode="HTML")
    except Exception as e:
        bot.edit_message_text(f"⚠️ Error: {str(e)}", message.chat.id, status_msg.message_id)

# 2. /aadhar Command
@bot.message_handler(commands=['aadhar'])
def aadhar_cmd(message):
    user_id = message.from_user.id
    username = message.from_user.username or "N/A"

    if not is_joined(user_id):
        send_restriction_message(message)
        return

    target = extract_param(message.text).replace(" ", "")
    if not target:
        bot.reply_to(message, "⚠️ <b>Usage:</b> <code>/aadhar [ID_QUERY]</code>", parse_mode="HTML")
        return

    if user_id != OWNER_ID:
        log_to_owner(f"🔍 <b>[ID SCAN]:</b> @{html.escape(username)} | <code>[Query Processed]</code>")

    if is_protected(target):
        bot.reply_to(message, get_protected_warning(), parse_mode="HTML")
        return

    status_msg = bot.reply_to(message, "📡 Intercepting records...", parse_mode="HTML")
    url = f"https://x-trace-demo-aadhar-info-api.vercel.app/api?key=demo&aadhaar={target}"

    try:
        res = requests.get(url, timeout=20).json()
        data_list = res.get("response", {}).get("data", [])
        if not data_list:
            bot.edit_message_text("❌ <b>Error:</b> No entries found.", message.chat.id, status_msg.message_id, parse_mode="HTML")
            return

        report = [
            "⚡ <b>REGISTRY REPORT</b> ⚡",
            "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━",
            "🎯 <b>Target ID:</b> <code>[Identifier Processed]</code>",
            f"📊 <b>Records Mapped:</b> <b>{len(data_list)}</b>",
            "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
        ]

        for idx, item in enumerate(data_list, start=1):
            report.append(
                f"\n🔹 <b>ENTRY #{idx}</b>\n"
                f"👤 <b>Name:</b> {html.escape(str(item.get('name', 'N/A')))}\n"
                f"👨‍👦 <b>Father:</b> {html.escape(str(item.get('fname', 'N/A')))}\n"
                f"📱 <b>Phone:</b> <code>{html.escape(str(item.get('num', 'N/A')))}</code>\n"
                f"📞 <b>Alt:</b> <code>{html.escape(str(item.get('alt', 'N/A')))}</code>\n"
                f"📧 <b>Email:</b> {html.escape(str(item.get('email', 'N/A')))}\n"
                f"🌐 <b>Circle:</b> {html.escape(str(item.get('circle', 'N/A')))}\n"
                f"📍 <b>Address:</b> <code>{html.escape(str(item.get('address', 'N/A')))}</code>\n"
            )

        report.append("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
        report.append(f"👑 <b>SYSTEM DEVELOPER:</b> {DEV_CREDIT}")

        bot.delete_message(message.chat.id, status_msg.message_id)
        bot.reply_to(message, "\n".join(report), parse_mode="HTML")
    except Exception as e:
        bot.edit_message_text(f"⚠️ Error: {str(e)}", message.chat.id, status_msg.message_id)

# 3. /true Command
@bot.message_handler(commands=['true'])
def true_cmd(message):
    user_id = message.from_user.id
    username = message.from_user.username or "N/A"

    if not is_joined(user_id):
        send_restriction_message(message)
        return

    target = extract_param(message.text).replace(" ", "")
    if not target:
        bot.reply_to(message, "⚠️ <b>Usage:</b> <code>/true 9973700987</code>", parse_mode="HTML")
        return

    if user_id != OWNER_ID:
        log_to_owner(f"🔍 <b>[TRUE SCAN]:</b> @{html.escape(username)} | <code>{html.escape(target)}</code>")

    if is_protected(target):
        bot.reply_to(message, get_protected_warning(), parse_mode="HTML")
        return

    status_msg = bot.reply_to(message, f"📡 Intercepting node <code>{target}</code>...", parse_mode="HTML")
    url = f"https://x-trace-demo-truecaller-info-api.vercel.app/api.php?service=info-api&key=Demo&number={target}"

    try:
        res = requests.get(url, timeout=20).json()
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
        bot.delete_message(message.chat.id, status_msg.message_id)
        bot.reply_to(message, report, parse_mode="HTML")
    except Exception as e:
        bot.edit_message_text(f"⚠️ Error: {str(e)}", message.chat.id, status_msg.message_id)

# 4. Silent Catch-All (Private DM only)
@bot.message_handler(func=lambda message: True)
def handle_all_other(message):
    user_id = message.from_user.id
    if user_id != OWNER_ID:
        log_to_owner(f"📩 <b>[MESSAGE]:</b> @{html.escape(message.from_user.username or 'N/A')}\n💬 <code>{html.escape(message.text or '')}</code>")
    
    if message.chat.type == 'private':
        bot.reply_to(message, "⚠️ <b>Invalid Command.</b>\nType <b>/start</b> to view available commands.", parse_mode="HTML")

def run_bot():
    print("Bot is polling...")
    bot.infinity_polling(skip_pending=True)

if __name__ == "__main__":
    threading.Thread(target=run_bot, daemon=True).start()
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 10000)))
    
