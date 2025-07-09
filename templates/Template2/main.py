
# TEMPLATE 2 - DARKN8 BOT TEMPLATE (Structured for BotBusiness)

# This is designed to be applied when a user selects Template 2 from the BotMaker

from telebot import TeleBot, types 
import  json 
import os

API_TOKEN = "YOUR_TEMPLATE2_BOT_TOKEN"  # To be replaced dynamically OWNER_ID = 123456789  # Will be set when the bot is created

bot = TeleBot(API_TOKEN)

settings_file = "settings_template2.json"

# Load or initialize settings

def load_settings(): if os.path.exists(settings_file): with open(settings_file, "r") as f: return json.load(f) return { "referral_reward": 10, "min_withdraw": 50, "bonus_amount": 20, "currency": "NGN", "channels": ["@DARKN80", "@Darkn8botmaker"] }

settings = load_settings()

# Save settings

def save_settings(): with open(settings_file, "w") as f: json.dump(settings, f, indent=2)

# Start

@bot.message_handler(commands=['start']) def start(message): user_id = message.from_user.id text = ( "🤖 <b>Welcome to Your Custom Bot</b>\n\n" f"💰 Bonus: <b>{settings['bonus_amount']} {settings['currency']}</b>\n" f"💸 Min Withdraw: <b>{settings['min_withdraw']} {settings['currency']}</b>\n" f"👥 Invite Friends and Earn <b>{settings['referral_reward']} {settings['currency']}</b> per invite." ) bot.send_message(message.chat.id, text, parse_mode="HTML")

#Admin Access

@bot.message_handler(commands=['adminaccess']) def admin_access(message): if message.from_user.id != OWNER_ID: return markup = types.ReplyKeyboardMarkup(resize_keyboard=True) markup.row("Set Referral Reward", "Set Min Withdraw") markup.row("Set Bonus", "Set Currency") bot.send_message(message.chat.id, "⚙️ Admin Panel", reply_markup=markup)

@bot.message_handler(func=lambda m: m.text == "Set Referral Reward") def set_ref(message): bot.send_message(message.chat.id, "💰 Send new referral reward amount:") bot.register_next_step_handler(message, save_ref)

def save_ref(message): try: settings["referral_reward"] = int(message.text.strip()) save_settings() bot.send_message(message.chat.id, "✅ Referral reward updated.") except: bot.send_message(message.chat.id, "❌ Invalid number.")

@bot.message_handler(func=lambda m: m.text == "Set Min Withdraw") def set_withdraw(message): bot.send_message(message.chat.id, "💸 Send new minimum withdrawal amount:") bot.register_next_step_handler(message, save_withdraw)

def save_withdraw(message): try: settings["min_withdraw"] = int(message.text.strip()) save_settings() bot.send_message(message.chat.id, "✅ Min withdraw updated.") except: bot.send_message(message.chat.id, "❌ Invalid number.")

@bot.message_handler(func=lambda m: m.text == "Set Bonus") def set_bonus(message): bot.send_message(message.chat.id, "🎁 Send new bonus amount:") bot.register_next_step_handler(message, save_bonus)

def save_bonus(message): try: settings["bonus_amount"] = int(message.text.strip()) save_settings() bot.send_message(message.chat.id, "✅ Bonus updated.") except: bot.send_message(message.chat.id, "❌ Invalid number.")

@bot.message_handler(func=lambda m: m.text == "Set Currency") def set_currency(message): bot.send_message(message.chat.id, "🌍 Send new currency code (e.g. NGN, USD):") bot.register_next_step_handler(message, save_currency)

def save_currency(message): settings["currency"] = message.text.strip().upper() save_settings() bot.send_message(message.chat.id, "✅ Currency updated.")

bot.infinity_polling()
