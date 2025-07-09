# DARKN8 BotMaker - Main Creator Bot (Termux Compatible)

# Requirements: pyTelegramBotAPI

import telebot from telebot import types import os import json

# API_TOKEN = 'YOUR_CREATOR_BOT_TOKEN' bot = telebot.TeleBot(API_TOKEN)

print("🤖 Bot is running...")

# Store data per bot

bot_settings = {}  # Stores settings per bot (template, owner, config) user_bots = {}  # user_id -> list of created bots

# Helper function to load or initialize a bot config

def get_bot_config(bot_token): path = f"created_bots/{bot_token}/config.json" if os.path.exists(path): with open(path, 'r') as f: return json.load(f) return { "owner_id": None, "template": None, "mandatory_channels": [], "settings": {} }

# Helper function to save bot config

def save_bot_config(bot_token, config): path = f"created_bots/{bot_token}" os.makedirs(path, exist_ok=True) with open(f"{path}/config.json", 'w') as f: json.dump(config, f, indent=2)

# Admin access panel (owner per bot)

@bot.message_handler(commands=['adminaccess']) def admin_access(message): user_id = str(message.from_user.id) current_bot_token = get_current_bot_token(user_id)  # Assume this tracks last bot edited if not current_bot_token: bot.reply_to(message, "❌ You haven't created or selected a bot yet.") return

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
markup.add("📢 Set Join Channels")
bot.send_message(message.chat.id, "⚙️ Admin Panel: Choose an option", reply_markup=markup)

# --- Must Join Channels Setup ---

@bot.message_handler(func=lambda m: m.text == "📢 Set Join Channels") def handle_set_join_channels(message): bot.send_message(message.chat.id, "🔗 Send the list of mandatory channels separated by spaces (e.g. @chan1 @chan2):") bot.register_next_step_handler(message, save_join_channels)

def save_join_channels(message): user_id = str(message.from_user.id) current_bot_token = get_current_bot_token(user_id) config = get_bot_config(current_bot_token) channels = message.text.strip().split() config["mandatory_channels"] = channels save_bot_config(current_bot_token, config) bot.send_message(message.chat.id, f"✅ Mandatory channels set: {' '.join(channels)}")

--- Join check function (used in bots created from templates) ---

def has_joined_mandatory(user_id, bot_token): config = get_bot_config(bot_token) for channel in config.get("mandatory_channels", []): try: member = bot.get_chat_member(channel, user_id) if member.status not in ['member', 'administrator', 'creator']: return False except: return False return True

# Dummy: Get current bot a user is managing (can be replaced with actual tracking logic)

def get_current_bot_token(user_id): # This function should retrieve the selected bot token by the user from storage/session try: with open(f"user_selected_bot/{user_id}.txt", "r") as f: return f.read().strip() except: return None

bot.infinity_polling()

