# Template 1 - DARKN8 BotMaker (Integrated with Admin Panel)

# Created bot script (Python) with adminaccess + full functionality

import telebot 
from telebot import types 
import json 
import os

API_TOKEN = 'PUT_YOUR_BOT_TOKEN_HERE' bot = telebot.TeleBot(API_TOKEN)

# Load settings

config_path = 'config.json' if os.path.exists(config_path): with open(config_path, 'r') as f: settings = json.load(f) else: settings = { "owner_id": None, "currency": "NGN", "referral_reward": 5, "min_withdraw": 50, "max_withdraw": 5000, "bonus": 0, "mandatory_channels": ["@DARKN80"], "tasks": [] }

# Save settings

def save_config(): with open(config_path, 'w') as f: json.dump(settings, f, indent=2)

# Memory storage for users

user_data = {}

# Start command with must join logic

@bot.message_handler(commands=['start']) def start(message): user_id = message.from_user.id

if not has_joined_mandatory(user_id):
    markup = types.InlineKeyboardMarkup(row_width=2)
    for ch in settings['mandatory_channels']:
        markup.add(types.InlineKeyboardButton(f"Join {ch}", url=f"https://t.me/{ch.lstrip('@')}", callback_data="join"))
    markup.add(types.InlineKeyboardButton("✅ Proceed", callback_data="check_join"))

    bot.send_message(message.chat.id, "🚀 *Welcome!*\n\nPlease join all required channels to proceed:", parse_mode="Markdown", reply_markup=markup)
    return

# Save new user
if user_id not in user_data:
    user_data[user_id] = {
        "balance": settings['bonus'],
        "referrals": [],
        "wallet": None
    }

show_main_menu(message)

# Check channel join status

@bot.callback_query_handler(func=lambda call: call.data == "check_join") def check_join_status(call): if has_joined_mandatory(call.from_user.id): start(call.message) else: bot.answer_callback_query(call.id, "🚫 You must join all required channels.", show_alert=True)

Check if user joined all channels

def has_joined_mandatory(user_id): for ch in settings['mandatory_channels']: try: member = bot.get_chat_member(ch, user_id) if member.status not in ["member", "administrator", "creator"]: return False except: return False return True

# Main menu

def show_main_menu(message): markup = types.ReplyKeyboardMarkup(resize_keyboard=True) markup.row("💰 Wallet", "📲 Refer & Earn") markup.row("📊 Statistics", "🎯 Tasks") markup.row("💸 Withdraw")

bot.send_message(message.chat.id, "🎉 Welcome! You can now access your dashboard.", reply_markup=markup)

# Wallet

@bot.message_handler(func=lambda m: m.text == "💰 Wallet") def wallet(message): user = user_data.get(message.from_user.id, {}) bal = user.get("balance", 0) ref = len(user.get("referrals", [])) per_ref = settings['referral_reward'] currency = settings['currency'] bot.reply_to(message, f"💼 Balance: {bal} {currency}\n👥 Total Invites: {ref}\n💵 Per Invite: {per_ref} {currency}\n\nInvite friends to earn more {currency}!")

# Refer & Earn

@bot.message_handler(func=lambda m: m.text == "📲 Refer & Earn") def refer_earn(message): link = f"https://t.me/{bot.get_me().username}?start={message.from_user.id}" bot.reply_to(message, f"🔗 Share this link to invite users:\n{link}")

# Withdraw

@bot.message_handler(func=lambda m: m.text == "💸 Withdraw") def withdraw(message): bot.send_message(message.chat.id, "💼 Send your withdrawal address:") bot.register_next_step_handler(message, save_wallet)

# Save wallet

def save_wallet(message): user_data.setdefault(message.from_user.id, {})["wallet"] = message.text bot.send_message(message.chat.id, "✅ Wallet saved! Now enter amount to withdraw:") bot.register_next_step_handler(message, process_withdraw)

# Process withdrawal

def process_withdraw(message): try: amount = float(message.text) user = user_data.get(message.from_user.id, {}) balance = user.get("balance", 0)

if amount < settings['min_withdraw']:
        bot.send_message(message.chat.id, f"❌ Minimum withdrawal is {settings['min_withdraw']} {settings['currency']}")
        return

    if amount > balance:
        bot.send_message(message.chat.id, "❌ Insufficient balance.")
        return

    user["balance"] -= amount
    wallet = user.get("wallet", "Not Set")
    bot.send_message(message.chat.id, f"✅ Your withdrawal of {amount} {settings['currency']} has been submitted!\n💼 Wallet: {wallet}")

    # Notify admin
    bot.send_message(settings['owner_id'], f"📤 New Withdrawal\n👤 User: {message.from_user.first_name} (@{message.from_user.username})\n💰 Amount: {amount} {settings['currency']}\n💼 Wallet: {wallet}")

except:
    bot.send_message(message.chat.id, "❌ Invalid amount.")

# Tasks section

@bot.message_handler(func=lambda m: m.text == "🎯 Tasks") def show_tasks(message): if not settings['tasks']: bot.send_message(message.chat.id, "📭 No tasks available yet.") return

msg = "📝 Tasks to complete:\n\n"
for i, task in enumerate(settings['tasks'], 1):
    msg += f"{i}. {task}\n"
bot.send_message(message.chat.id, msg)

# Stats

@bot.message_handler(func=lambda m: m.text == "📊 Statistics") def stats(message): bot.send_message(message.chat.id, f"📈 Total Users: {len(user_data)}\n💰 Total Balance: {sum(u.get('balance', 0) for u in user_data.values())} {settings['currency']}")

bot.infinity_polling()

