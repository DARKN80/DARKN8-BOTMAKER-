import telebot
from telebot import types
import json 
import os

# === Load bot token and config ===

with open("config.json") as f: config = json.load(f) bot_token = config.get("bot_token") owner_id = config.get("owner_id") currency = config.get("settings", {}).get("currency", "NGN") per_ref = config.get("settings", {}).get("referral_reward", 1) mandatory = config.get("mandatory_channels", [])

if "@DARKN80" not in mandatory: mandatory.append("@DARKN80")

bot = telebot.TeleBot(bot_token) user_wallets = {} user_balances = {} user_referrals = {}

print("🚀 Template 3 Bot is running...")

# === START ===

@bot.message_handler(commands=['start']) def start(message): user_id = message.from_user.id keyboard = types.InlineKeyboardMarkup(row_width=2) for i in range(0, len(mandatory) - 1, 2): keyboard.add( types.InlineKeyboardButton(f"📣 Must Join {i+1}", url=f"https://t.me/{mandatory[i].replace('@', '')}"), types.InlineKeyboardButton(f"📣 Must Join {i+2}", url=f"https://t.me/{mandatory[i+1].replace('@', '')}") ) if len(mandatory) % 2 != 0: keyboard.add(types.InlineKeyboardButton(f"📣 Must Join {len(mandatory)}", url=f"https://t.me/{mandatory[-1].replace('@', '')}")) keyboard.add(types.InlineKeyboardButton("✅ Proceed", callback_data="check_join"))

text = (
    "<b>Welcome</b>\n\n"
    "📣 <b>JOIN OUR CHANNELS TO RECEIVE YOUR WITHDRAWALS:</b>"
)
bot.send_message(user_id, text, parse_mode="HTML", reply_markup=keyboard)

# === JOIN CHECK ===

@bot.callback_query_handler(func=lambda call: call.data == "check_join") def check_join(call): user_id = call.from_user.id for channel in mandatory: try: member = bot.get_chat_member(chat_id=channel, user_id=user_id) if member.status not in ['member', 'administrator', 'creator']: bot.answer_callback_query(call.id, "🚫 Please join all required channels first.", show_alert=True) return except: bot.answer_callback_query(call.id, "⚠️ Error checking one of the channels.", show_alert=True) return

welcome_text = (
    "🎉 <b>You're In!</b>\n\n"
    "Welcome to your dashboard. Use the menu below to earn, invite, and withdraw."
)
menu = types.ReplyKeyboardMarkup(resize_keyboard=True)
menu.add("💰 Wallet", "📲 Refer & Earn")
menu.add("📊 Statistics", "🎯 Tasks")
menu.add("💸 Withdraw")

bot.send_message(user_id, welcome_text, parse_mode="HTML", reply_markup=menu)

# === WALLET ===

@bot.message_handler(func=lambda m: m.text == "💰 Wallet") def wallet_menu(message): uid = message.from_user.id wallet = user_wallets.get(uid, "Not Set") text = f"💼 Your wallet address is:\n<code>{wallet}</code>" markup = types.InlineKeyboardMarkup() markup.add(types.InlineKeyboardButton("✏️ Set Wallet", callback_data="set_wallet")) bot.send_message(uid, text, parse_mode="HTML", reply_markup=markup)

@bot.callback_query_handler(func=lambda call: call.data == "set_wallet") def ask_wallet(call): bot.send_message(call.message.chat.id, "Send your wallet address:") bot.register_next_step_handler(call.message, save_wallet)

def save_wallet(message): user_wallets[message.from_user.id] = message.text.strip() bot.send_message(message.chat.id, "✅ Wallet address saved!")

# === REFER ===

@bot.message_handler(func=lambda m: m.text == "📲 Refer & Earn") def refer_info(message): uid = message.from_user.id invite_link = f"https://t.me/{bot.get_me().username}?start={uid}" total_refs = user_referrals.get(uid, 0) text = ( f"<b>👥 Referral Program</b>\n\n" f"🔗 Your Invite Link:\n{invite_link}\n\n" f"💰 Per Invite: {per_ref} {currency}\n" f"🎯 Total Invites: {total_refs}\n\n" f"Share your link to earn more!" ) bot.send_message(uid, text, parse_mode="HTML")

# === TASKS ===

@bot.message_handler(func=lambda m: m.text == "🎯 Tasks") def tasks(message): text = "📝 No active tasks yet. Tasks will appear here when set by the admin." bot.send_message(message.chat.id, text)

# === STATISTICS ===

@bot.message_handler(func=lambda m: m.text == "📊 Statistics") def stats(message): total_users = len(user_wallets) total_withdrawn = sum(user_balances.values()) text = ( f"📊 Bot Stats:\n\n" f"👥 Total Users: {total_users}\n" f"💸 Total Paid Out: {total_withdrawn} {currency}\n" f"🤖 Created with @DARKN8BOTMAKERBOT" ) bot.send_message(message.chat.id, text)

# === WITHDRAW ===

@bot.message_handler(func=lambda m: m.text == "💸 Withdraw") def withdraw(message): uid = message.from_user.id wallet = user_wallets.get(uid) if not wallet: bot.send_message(uid, "⚠️ Please set your wallet first via 💰 Wallet") return bot.send_message(uid, f"💵 How much {currency} do you want to withdraw?") bot.register_next_step_handler(message, process_withdraw)

def process_withdraw(message): uid = message.from_user.id try: amount = float(message.text) except: bot.send_message(uid, "❌ Invalid amount.") return

current_balance = user_balances.get(uid, 0)
if amount > current_balance:
    bot.send_message(uid, "❌ Insufficient balance.")
    return

user_balances[uid] = current_balance - amount
bot.send_message(uid, f"✅ Withdrawal request of {amount} {currency} received!\n⏳ You will be paid shortly.")

bot.send_message("@payout119", f"📤 New Withdrawal\nUser ID: {uid}\nAmount: {amount} {currency}\nWallet: {user_wallets[uid]}")

bot.infinity_polling()

