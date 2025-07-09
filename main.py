
# DARKN8 BotMaker - Template1 Botbusiness

# Requirements: pyTelegramBotAPI

import telebot from telebot import types import os import json

API_TOKEN = 'YOUR_CREATED_BOT_TOKEN' DATA_FILE = 'bot_data.json'

bot = telebot.TeleBot(API_TOKEN) print("🤖 Bot is running...")

# Load creator and settings data

if os.path.exists(DATA_FILE): with open(DATA_FILE, 'r') as f: bot_data = json.load(f) else: bot_data = { "creator_id": 123456789,  # Will be updated when created "channels": ["@DARKN80", "@Darkn8botmaker"], "welcome_text": "🤗 <b>Welcome to DARKN8 BotMaker bot</b>\n\nCreate And Build Free Telegram Bots Here\n\nNow, Join Our Official Channels." } with open(DATA_FILE, 'w') as f: json.dump(bot_data, f, indent=2)

creator_id = bot_data.get("creator_id")

# /start command shows stored welcome

@bot.message_handler(commands=['start']) def send_start(message): chat_id = message.chat.id markup = types.InlineKeyboardMarkup() for ch in bot_data.get("channels", []): markup.add(types.InlineKeyboardButton(f"📢 {ch}", url=f"https://t.me/{ch.strip('@')}")) markup.add(types.InlineKeyboardButton("✅ Joined", callback_data="joined"))

bot.send_message(chat_id, bot_data.get("welcome_text", "Welcome"), parse_mode="HTML", reply_markup=markup)

# Only the creator can access admin

@bot.message_handler(commands=['adminaccess']) def admin_access(message): user_id = message.from_user.id if user_id != creator_id: return  # Do not reply

markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
markup.add("📄 Bot Info", "🌐 Set Currency")
markup.add("💰 Set Referral Reward", "🎁 Set Bonus")
markup.add("🎯 Min Withdraw", "✋ Max Withdraw")
markup.add("🔗 Set Start Menu Links", "➕ Add/Remove Balance")
markup.add("🔴 Ban/Unban User", "📣 Broadcast Message")
markup.add("✅ Bot (ON)", "❌ Verification (OFF)")
markup.add("💸 Withdrawals (ON)", "🚫 New User Notification")
markup.add("🎨 Change Template", "🌍 Change Language")
bot.send_message(message.chat.id, "⚙️ Admin Panel: Choose an option", reply_markup=markup)

@bot.message_handler(func=lambda m: m.text == "➕ Add/Remove Balance") def handle_balance_prompt(message): bot.send_message(message.chat.id, "💳 Send command like:\nadd USERID AMOUNT\nremove USERID AMOUNT") bot.register_next_step_handler(message, process_balance_command)

def process_balance_command(message): try: parts = message.text.split() cmd, uid, amount = parts[0], int(parts[1]), int(parts[2]) uid = str(uid) if uid not in bot_data: bot_data[uid] = {"balance": 0} if cmd == "add": bot_data[uid]["balance"] += amount bot.reply_to(message, f"✅ Added {amount} to user {uid}. New balance: {bot_data[uid]['balance']}") elif cmd == "remove": bot_data[uid]["balance"] -= amount bot.reply_to(message, f"✅ Removed {amount} from user {uid}. New balance: {bot_data[uid]['balance']}") else: bot.reply_to(message, "❌ Invalid command. Use 'add' or 'remove'") with open(DATA_FILE, 'w') as f: json.dump(bot_data, f, indent=2) except Exception as e: bot.reply_to(message, f"❌ Error: {str(e)}")

# Placeholder for features

@bot.message_handler(func=lambda m: m.text in [ "📄 Bot Info", "🌐 Set Currency", "💰 Set Referral Reward", "🎁 Set Bonus", "🎯 Min Withdraw", "✋ Max Withdraw", "🔗 Set Start Menu Links", "🔴 Ban/Unban User", "📣 Broadcast Message", "✅ Bot (ON)", "❌ Verification (OFF)", "💸 Withdrawals (ON)", "🚫 New User Notification", "🎨 Change Template", "🌍 Change Language"]) def handle_placeholder(message): bot.reply_to(message, f"⚠️ Feature '{message.text}' is under development.")

bot.infinity_polling()

