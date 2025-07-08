# DARKN8 BotMaker - Main Creator Bot (PythonAnywhere or Render)
# Requirements: pyTelegramBotAPI

import telebot
from telebot import types

API_TOKEN = '7679897180:AAGiMylpZzMVMX8U6TwAgeXD_kYMuvB_2As'  # Replace with your actual bot token
OWNER_ID = 7752955793  # Replace with your Telegram ID
MANDATORY_CHANNELS = ["@DARKN80", "@Darkn8botmaker"]

bot = telebot.TeleBot(API_TOKEN)
user_bots = {}  # Dictionary to store created bots by user_id

# 🔍 Check if user has joined all mandatory channels
def has_joined_all_channels(user_id):
    for channel in MANDATORY_CHANNELS:
        try:
            member = bot.get_chat_member(channel, user_id)
            if member.status not in ['member', 'administrator', 'creator']:
                return False
        except:
            return False
    return True

# 🚀 Start Command
@bot.message_handler(commands=['start'])
def send_welcome(message):
    chat_id = message.chat.id
    user_id = message.from_user.id

    if not has_joined_all_channels(user_id):
        join_msg = "🚫 You must join all channels to use this bot."
        join_markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        for ch in MANDATORY_CHANNELS:
            join_markup.add(types.KeyboardButton(f"📢 Join {ch}"))
        join_markup.add(types.KeyboardButton("✅ I've Joined"))
        bot.send_message(chat_id, join_msg, reply_markup=join_markup)
        return

    menu = types.ReplyKeyboardMarkup(resize_keyboard=True)
    menu.row("📦 Create Bot", "🤖 My Bots")
    menu.row("🛠️ Tools", "📢 Promotion")
    bot.send_message(chat_id, "👋 Welcome to DARKN8 BotMaker!", reply_markup=menu)

# 📩 Text Message Handler
@bot.message_handler(func=lambda message: True)
def handle_text(message):
    user_id = message.from_user.id
    chat_id = message.chat.id
    text = message.text.strip()

    if text == "✅ I've Joined":
        if has_joined_all_channels(user_id):
            menu = types.ReplyKeyboardMarkup(resize_keyboard=True)
            menu.row("📦 Create Bot", "🤖 My Bots")
            menu.row("🛠️ Tools", "📢 Promotion")
            bot.send_message(chat_id, "✅ Verified! Welcome to DARKN8 BotMaker.", reply_markup=menu)
        else:
            bot.send_message(chat_id, "❗ You must join all channels first.")

    elif text == "📦 Create Bot":
        bot.send_message(chat_id, "🤖 Go to @BotFather, create a new bot, then send the API token here:")
        bot.register_next_step_handler(message, handle_token_submission)

    elif text == "🤖 My Bots":
        bots = user_bots.get(user_id, [])
        if not bots:
            bot.send_message(chat_id, "😕 You haven't created any bots yet.")
        else:
            text = "🤖 Your Bots:\n" + '\n'.join(bots)
            bot.send_message(chat_id, text)

    elif text == "🛠️ Tools":
        bot.send_message(chat_id, "🔧 Tools:\n1️⃣ Remove Forward Tag ➡ @forwardtag0bot")

    elif text == "📢 Promotion":
        bot.send_message(chat_id, "📢 Free Promotion Available!\nDM @DARKN8002 with proof of funds to get started.")

# 🔑 Handle Bot Token Submission
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
            f"✅ Bot created: {bot_username}\n\nSend /adminaccess in your bot to continue setup.",
            reply_markup=template_menu())

    except Exception as e:
        bot.send_message(chat_id, f"❌ Error: {str(e)}")

# 🎨 Template Selection Menu
def template_menu():
    markup = types.InlineKeyboardMarkup()
    markup.row(
        types.InlineKeyboardButton("Template 1", callback_data='template_1'),
        types.InlineKeyboardButton("Template 2", callback_data='template_2')
    )
    markup.row(
        types.InlineKeyboardButton("Template 3", callback_data='template_3')
    )
    return markup

# 🧠 Template Assignment Handler
@bot.callback_query_handler(func=lambda call: call.data.startswith('template_'))
def handle_template_choice(call):
    template_id = call.data.split('_')[1]
    bot.send_message(call.message.chat.id,
        f"🎉 Template {template_id} has been applied to your bot.\n\n✅ Mandatory channels set to: {', '.join(MANDATORY_CHANNELS)}")

# 🟢 Run the bot
bot.infinity_polling()
