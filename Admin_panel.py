#DARKN8 Template AdminAccess with Full Task Management

import telebot
from telebot import types
import os 
import json

API_TOKEN = 'YOUR_BOT_API_TOKEN' bot = telebot.TeleBot(API_TOKEN)

# === CONFIG STORAGE ===

def get_bot_config(): path = "config.json" if os.path.exists(path): with open(path, 'r') as f: return json.load(f) return { "owner_id": None, "mandatory_channels": [], "tasks": [], "currency": "NGN", "referral_reward": 0.5 }

def save_bot_config(config): with open("config.json", 'w') as f: json.dump(config, f, indent=2)

# === ADMIN ACCESS ===

@bot.message_handler(commands=['adminaccess']) def admin_panel(message): user_id = str(message.from_user.id) config = get_bot_config()

if str(config.get("owner_id")) != user_id:
    bot.reply_to(message, "❌ You are not the owner of this bot.")
    return

markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
markup.add("📄 Bot Info", "🌐 Set Currency")
markup.add("💰 Set Referral Reward", "📢 Set Join Channels")
markup.add("➕ Add Task", "📋 View Tasks", "❌ Delete Task")
bot.send_message(message.chat.id, "⚙️ Admin Panel - Select Option:", reply_markup=markup)

# === CURRENCY ===

@bot.message_handler(func=lambda m: m.text == "🌐 Set Currency") def ask_currency(message): bot.send_message(message.chat.id, "💱 Send your preferred currency symbol (e.g. NGN, ₦, USD):") bot.register_next_step_handler(message, save_currency)

def save_currency(message): config = get_bot_config() config['currency'] = message.text.strip() save_bot_config(config) bot.send_message(message.chat.id, f"✅ Currency set to {message.text.strip()}")

# === REFERRAL REWARD ===

@bot.message_handler(func=lambda m: m.text == "💰 Set Referral Reward") def ask_reward(message): bot.send_message(message.chat.id, "💸 Enter reward per referral:") bot.register_next_step_handler(message, save_reward)

def save_reward(message): try: amount = float(message.text.strip()) config = get_bot_config() config['referral_reward'] = amount save_bot_config(config) bot.send_message(message.chat.id, f"✅ Referral reward set to {amount}") except: bot.send_message(message.chat.id, "❌ Invalid input. Try again.")

# === SET JOIN CHANNELS ===

@bot.message_handler(func=lambda m: m.text == "📢 Set Join Channels") def ask_channels(message): bot.send_message(message.chat.id, "📣 Send channel usernames separated by space (e.g. @chan1 @chan2):") bot.register_next_step_handler(message, save_channels)

def save_channels(message): config = get_bot_config() channels = message.text.strip().split() config['mandatory_channels'] = channels save_bot_config(config) bot.send_message(message.chat.id, f"✅ Channels set: {' | '.join(channels)}")

# === ADD TASK ===

@bot.message_handler(func=lambda m: m.text == "➕ Add Task") def start_add_task(message): bot.send_message(message.chat.id, "📝 Send task title:") bot.register_next_step_handler(message, receive_task_title)

def receive_task_title(message): title = message.text.strip() bot.send_message(message.chat.id, "🎯 Send task reward amount:") bot.register_next_step_handler(message, lambda msg: receive_task_reward(msg, title))

def receive_task_reward(message, title): try: reward = float(message.text.strip()) bot.send_message(message.chat.id, "🔗 Send the task URL or link:") bot.register_next_step_handler(message, lambda msg: save_new_task(msg, title, reward)) except: bot.send_message(message.chat.id, "❌ Invalid reward. Task cancelled.")

def save_new_task(message, title, reward): url = message.text.strip() config = get_bot_config() task = {"title": title, "reward": reward, "link": url} config['tasks'].append(task) save_bot_config(config) bot.send_message(message.chat.id, f"✅ Task added: {title} → {reward} {config['currency']}")

# === VIEW TASKS ===

@bot.message_handler(func=lambda m: m.text == "📋 View Tasks") def show_tasks(message): config = get_bot_config() tasks = config.get("tasks", []) if not tasks: bot.send_message(message.chat.id, "📭 No tasks added yet.") else: msg = "📋 Current Tasks: \n" for i, t in enumerate(tasks, 1): msg += f"{i}. {t['title']} → {t['reward']} {config['currency']}\n" bot.send_message(message.chat.id, msg, parse_mode="Markdown")

# === DELETE TASK ===

@bot.message_handler(func=lambda m: m.text == "❌ Delete Task")

def ask_delete_task(message): config = get_bot_config() tasks = config.get("tasks", []) if not tasks: bot.send_message(message.chat.id, "❌ No tasks to delete.") return msg = "🗑️ Select task number to delete:\n" for i, t in enumerate(tasks, 1): msg += f"{i}. {t['title']}\n" bot.send_message(message.chat.id, msg, parse_mode="Markdown") bot.register_next_step_handler(message, confirm_task_delete)

def confirm_task_delete(message): try: idx = int(message.text.strip()) - 1 config = get_bot_config() task = config['tasks'].pop(idx) save_bot_config(config) bot.send_message(message.chat.id, f"✅ Task '{task['title']}' deleted.") except: bot.send_message(message.chat.id, "❌ Invalid input. Deletion cancelled.")

bot.infinity_polling()

