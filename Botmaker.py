# DARKN8 BotMaker - Termux Compatible
# Author: DARKN8
# Requirements: pyTelegramBotAPI

import telebot
from telebot import types

# 🔐 Configuration
API_TOKEN = '7679897180:AAEErLJcstZMKUSJ8nwIGU5Kx5ytXgf0rPA'  # Test Token
OWNER_ID = 7752955793  # Replace with your Telegram ID
MANDATORY_CHANNELS = ["@DARKN80", "@Darkn8botmaker"]  # Channels users must join

# 🤖 Initialize Bot
bot = telebot.TeleBot(API_TOKEN)
user_bots = {}  # Store created bots per user

print("🤖 Bot is running...")

# ✅ Function: Check if user joined all required channels
def has_joined_all_channels(user_id):
    for channel in MANDATORY_CHANNELS:
        try:
            member = bot.get_chat_member(channel, user_id)
            if member.status not in ['member', 'administrator', 'creator']:
                return False
        except:
            return False
    return True

# 🚪 /start Command
@bot.message_handler(commands=['start'])
def send_welcome(message):
    chat_id = message.chat.id
    user_id = message.from_user.id

    # 🌟 Welcome Text
    welcome_text = (
        "✨ <b>Welcome to DARKN8 BotMaker</b>\n\n"
        "🚀 Easily create your own Telegram bot in seconds.\n\n"
        "🔒 To get started, please join our required channels '
        "✅ After joining, click <b>I've Joined</b> below to continue."
    )

    # 🔘 Inline Buttons
    join_markup = types.InlineKeyboardMarkup()
    join_markup.add(
        types.InlineKeyboardButton("📢 Join @DARKN80", url="https://t.me/DARKN80"),
        types.InlineKeyboardButton("📢 Join @Darkn8botmaker", url="https://t.me/Darkn8botmaker")
    )
    join_markup.add(
        types.InlineKeyboardButton("✅ I've Joined", callback_data="check_joined")
    )

    bot.send_message(chat_id, welcome_text, reply_markup=join_markup, parse_mode='HTML')

# ✅ Handle Join Check
@bot.callback_query_handler(func=lambda call: call.data == "check_joined")
def check_joined_channels(call):
    user_id = call.from_user.id
    chat_id = call.message.chat.id

    if has_joined_all_channels(user_id):
        menu = types.ReplyKeyboardMarkup(resize_keyboard=True)
        menu.row("📦 Create Bot", "🤖 My Bots")
        menu.row("🛠️ Tools", "📢 Promotion", "🗑 Delete Bot")
        bot.send_message(chat_id, "✅ Access granted! You're in. Choose an option below.", reply_markup=menu)
    else:
        bot.answer_callback_query(call.id, "❗ Please make sure you've joined all channels.", show_alert=True)

# 🗨 Handle User Text Input
@bot.message_handler(func=lambda message: True)
def handle_text(message):
    user_id = message.from_user.id
    chat_id = message.chat.id
    text = message.text.strip()

    # ➕ Create Bot
    if text == "📦 Create Bot":
        bot.send_message(chat_id, "Choose a template to apply:", reply_markup=template_menu())

    # 🤖 My Bots
    elif text == "🤖 My Bots":
        bots = user_bots.get(user_id, [])
        if not bots:
            bot.send_message(chat_id, "😕 You haven't created any bots yet.")
        else:
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
            markup.row("🔙 Back to Menu")
            for botname in bots:
                markup.row(f"🗑 Delete {botname}")
            bot.send_message(chat_id, "🤖 Your Bots:", reply_markup=markup)

    # 🗑 Delete Bot
    elif text.startswith("🗑 Delete"):
        botname = text.split("🗑 Delete ")[-1].strip()
        if user_id in user_bots and botname in user_bots[user_id]:
            user_bots[user_id].remove(botname)
            bot.send_message(chat_id, f"✅ {botname} has been deleted.")
        else:
            bot.send_message(chat_id, "❌ Bot not found.")

    # 🛠️ Tools
    elif text == "🛠️ Tools":
        bot.send_message(chat_id, "🔧 Tools:\n1️⃣ Remove Forward Tag ➡ @forwardtag0bot")

    # 📢 Promotion
    elif text == "📢 Promotion":
        bot.send_message(chat_id, "📢 Free Promotion Available!\nDM @DARKN8002 with proof of funds to get started.")

    # 🔙 Back
    elif text == "🔙 Back to Menu":
        menu = types.ReplyKeyboardMarkup(resize_keyboard=True)
        menu.row("📦 Create Bot", "🤖 My Bots")
        menu.row("🛠️ Tools", "📢 Promotion", "🗑 Delete Bot")
        bot.send_message(chat_id, "👋 Back to main menu:", reply_markup=menu)

# 🧩 Handle Template Selection
@bot.callback_query_handler(func=lambda call: call.data.startswith('template_'))
def handle_template_choice(call):
    user_id = call.from_user.id
    chat_id = call.message.chat.id
    bot.send_message(chat_id, "📬 Now, get your API Token from @BotFather and send it here:")
    bot.register_next_step_handler(call.message, handle_token_submission)

# 🔑 Handle Token Submission
def handle_token_submission(message):
    token = message.text.strip()
    user_id = message.from_user.id
    chat_id = message.chat.id

    if not has_joined_all_channels(user_id):
        bot.send_message(chat_id, "❗ You must join all required channels before creating a bot.")
        return

    if len(token.split(':')) != 2:
        bot.send_message(chat_id, "❌ Invalid token format. Please try again.")
        return

    try:
        new_bot = telebot.TeleBot(token)
        me = new_bot.get_me()
        bot_username = f"@{me.username}"

        if user_id not in user_bots:
            user_bots[user_id] = []
        user_bots[user_id].append(bot_username)

        bot.send_message(chat_id,
            f"✅ Bot created: {bot_username}\n\n📌 Send <code>/adminaccess</code> in your bot to continue setup.",
            parse_mode='HTML')
    except Exception as e:
        bot.send_message(chat_id, f"❌ Error: {str(e)}")

# 🧩 Template Menu Options
def template_menu():
    markup = types.InlineKeyboardMarkup()
    markup.row(
        types.InlineKeyboardButton("Template 1", callback_data='template_1'),
        types.InlineKeyboardButton("Template 2", callback_data='template_2')
    )
    markup.row(types.InlineKeyboardButton("Template 3", callback_data='template_3'))
    return markup

# 🔁 Run Bot Forever
bot.infinity_polling()
