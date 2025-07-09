# DARKN8 BotMaker - Admin Access Panel with Task + Multi-Template Support

# Requirements: pyTelegramBotAPI

import telebot from telebot import types import os import json

API_TOKEN = 'YOUR_CREATOR_BOT_TOKEN' bot = telebot.TeleBot(API_TOKEN) print("🤖 Bot is running...")

# Stores per-user bot data

bot_settings = {}  # bot_token -> config template_tasks = {}  # bot_token -> list of tasks

# Helper: Get bot config

def get_bot_config(bot_token): path = f"created_bots/{bot_token}/config.json" if os.path.exists(path): with open(path, 'r') as f: return json.load(f) return { "owner_id": None, "template": None, "mandatory_channels": [], "settings": {}, "tasks": [] }

# Helper: Save bot config

def save_bot_config(bot_token, config): path = f"created_bots/{bot_token}" os.makedirs(path, exist_ok=True) with open(f"{path}/config.json", 'w') as f: json.dump(config, f, indent=2)

# Get selected bot by user

def get_current_bot_token(user_id): try: with open(f"user_selected_bot/{user_id}.txt", "r") as f: return f.read().strip() except: return None

# Admin Access Command

@bot.message_handler(commands=['adminaccess']) def admin_access(message): user_id = str(message.from_user.id) current_bot_token = get_current_bot_token(user_id) if not current_bot_token: bot.reply_to(message, "❌ You haven't created or selected a bot yet.") return

config = get_bot_config(current_bot_token)
if str(config.get("owner_id")) != user_id:
    bot.reply_to(message, "❌ You are not the owner of this bot.")
    return

markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
markup.add("📄 Bot Info", "🌐 Set Currency")
markup.add("💰 Set Referral Reward", "🎁 Set Bonus")
markup.add("🎯 Min Withdraw", "✋ Max Withdraw")
markup.add("🔗 Set Start Menu Links", "➕ Add/Remove Balance")
markup.add("🔴 Ban/Unban User", "📣 Broadcast Message")
markup.add("✅ Bot (ON)", "❌ Verification (OFF)")
markup.add("💸 Withdrawals (ON)", "🚫 New User Notification")
markup.add("🎨 Change Template", "🌍 Change Language")
markup.add("📢 Set Join Channels", "📝 Add Task")
bot.send_message(message.chat.id, "⚙️ Admin Panel: Choose an option", reply_markup=markup)

# --- Must Join Channels ---

@bot.message_handler(func=lambda m: m.text == "📢 Set Join Channels") def handle_set_join_channels(message): bot.send_message(message.chat.id, "🔗 Send the list of mandatory channels separated by spaces (e.g. @chan1 @chan2):") bot.register_next_step_handler(message, save_join_channels)

def save_join_channels(message): user_id = str(message.from_user.id) current_bot_token = get_current_bot_token(user_id) config = get_bot_config(current_bot_token) channels = message.text.strip().split() config["mandatory_channels"] = ["@DARKN80"] + channels  # Add @DARKN80 automatically save_bot_config(current_bot_token, config) bot.send_message(message.chat.id, f"✅ Mandatory channels set: {' '.join(config['mandatory_channels'])}")

# --- Task Feature ---

@bot.message_handler(func=lambda m: m.text == "📝 Add Task") def handle_add_task(message): bot.send_message(message.chat.id, "📝 Send the task link or description:") bot.register_next_step_handler(message, save_task)

def save_task(message): user_id = str(message.from_user.id) current_bot_token = get_current_bot_token(user_id) config = get_bot_config(current_bot_token) task = message.text.strip() config.setdefault("tasks", []).append(task) save_bot_config(current_bot_token, config) bot.send_message(message.chat.id, f"✅ Task added: {task}")

# Used by bot templates:

def has_joined_mandatory(user_id, bot_token): config = get_bot_config(bot_token) for channel in config.get("mandatory_channels", []): try: member = bot.get_chat_member(channel, user_id) if member.status not in ['member', 'administrator', 'creator']: return False except: return False return True

bot.infinity_polling()

