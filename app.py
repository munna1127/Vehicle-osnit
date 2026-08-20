import os
import threading
import telebot
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

OWNER_ID = int(os.getenv("OWNER_ID", "6508791739"))
CHANNEL = "@tech_updates_india0763"
GROUP = "@allioneplace"
YOUTUBE_URL = "https://www.youtube.com/@hackeronall"
DEV_CREDIT = "@tomar_ji_99"

def log_to_owner(log_text):
    try:
        bot.send_message(OWNER_ID, log_text, parse_mode='HTML', disable_web_page_preview=True)
    except Exception:
        pass

def is_joined(user_id):
    if user_id == OWNER_ID:
        return True
    try:
        ch_member = bot.get_chat_member(CHANNEL, user_id)
        if ch_member.status not in ["member", "administrator", "creator"]:
            return False
        
        grp_member = bot.get_chat_member(GROUP, user_id)
        if grp_member.status not in ["member", "administrator", "creator"]:
            return False
            
        return True
    except Exception:
        # Fallback if bot is not admin in channels
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
        "Bot use karne ke liye channel aur group join karein, fir <b>/start</b> dabayein.",
        reply_markup=get_join_markup(),
        parse_mode="HTML"
    )

def extract_param(text):
    parts = text.strip().split(maxsplit=1)
    return parts[1].strip() if len(parts) > 1 else ""

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
        "⚡ <b>SYSTEM ACTIVE</b> ⚡\n"
        "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n\n"
        "🛠️ <b>COMMANDS:</b>\n"
        "👉 <code>/status</code> - Check bot health\n"
        "👉 <code>/help</code> - View documentation\n\n"
        "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n"
        f"👑 <b>DEVELOPER:</b> {DEV_CREDIT}"
    )
    bot.reply_to(message, welcome_text, parse_mode="HTML")

# STATUS / PING COMMAND
@bot.message_handler(commands=['status', 'help'])
def help_cmd(message):
    if not is_joined(message.from_user.id):
        send_restriction_message(message)
        return
    bot.reply_to(message, "✅ Service is running smoothly and ready for requests.", parse_mode="HTML")

# CATCH-ALL HANDLER
@bot.message_handler(func=lambda message: True)
def handle_all_other(message):
    user_id = message.from_user.id
    if user_id != OWNER_ID:
        log_to_owner(f"📩 <b>[MSG]:</b> @{html.escape(message.from_user.username or 'N/A')}\n💬 <code>{html.escape(message.text or '')}</code>")
    
    if message.chat.type == 'private':
        bot.reply_to(message, "⚠️ <b>Invalid Command.</b>\nType <b>/start</b> to view menu.", parse_mode="HTML")

def run_bot():
    print("Bot polling started...")
    bot.infinity_polling(skip_pending=True)

if __name__ == "__main__":
    # Start bot polling in a background daemon thread
    bot_thread = threading.Thread(target=run_bot, daemon=True)
    bot_thread.start()
    
    # Run Flask server with reloader disabled to avoid duplicate polling instances
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port, use_reloader=False)
