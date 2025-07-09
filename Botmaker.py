DARKN8 BotMaker - Main Creator Bot

Requirements: pyTelegramBotAPI

import telebot from telebot import types

Your Bot Token

API_TOKEN = '7679897180:AAEErLJcstZMKUSJ8nwIGU5Kx5ytXgf0rPA'

# Your Telegram ID

OWNER_ID = 7752955793

Channels users must join

MANDATORY_CHANNELS = ["@DARKN80", "@Darkn8botmaker"]

bot = telebot.TeleBot(API_TOKEN)

# Dictionary to store created bots by user_id

user_bots = {}

print("🤖 Bot is running...")

Function to check if user has joined all required channels

def has_joined_all_channels(user_id): for channel in MANDATORY_CHANNELS: try: member = bot.get_chat_member(channel, user_id) if member.status not in ['member', 'administrator', 'creator']: return False except: return False return True

# Handle the /start command

@bot.message_handler(commands=['start']) def send_start(message): chat_id = message.chat.id

# Welcome text with join instructions
welcome_text = (
    "🤗 <b>Welcome to DARKN8 BotMaker bot</b>\n\n"
    "Create And Build Free Telegram Bots Here\n\n"
    "Now, Join Our Official Channels."
)

# Inline join buttons
markup = types.InlineKeyboardMarkup()
markup.add(types.InlineKeyboardButton("📢 OFFICIAL CHANNEL 1", url="https://t.me/DARKN80"))
markup.add(types.InlineKeyboardButton("📢 OFFICIAL CHANNEL 2", url="https://t.me/Darkn8botmaker"))
markup.add(types.InlineKeyboardButton("✅ Joined", callback_data="joined"))

# Send welcome message
bot.send_message(chat_id, welcome_text, parse_mode="HTML", reply_markup=markup)

Check channel join after pressing 'Joined'

@bot.callback_query_handler(func=lambda call: call.data == "joined") def check_joined_channels(call): user_id = call.from_user.id chat_id = call.message.chat.id

if has_joined_all_channels(user_id):
    # Show main menu
    menu = types.ReplyKeyboardMarkup(resize_keyboard=True)
    menu.row("📦 Create Bot", "🤖 My Bots")
    menu.row("🛠️ Tools", "📢 Promotion", "🗑 Delete Bot")
    bot.send_message(chat_id, "✅ Access granted! You're in. Choose an option below.", reply_markup=menu)
else:
    bot.answer_callback_query(call.id, "❗ Please make sure you've joined all channels.", show_alert=True)

# Handle all text-based replies

@bot.message_handler(func=lambda message: True) def handle_text(message): user_id = message.from_user.id chat_id = message.chat.id text = message.text.strip()

if text == "📦 Create Bot":
    # Ask user to select a template
    bot.send_message(chat_id, "Choose a template first:", reply_markup=template_menu())

elif text == "🤖 My Bots":
    # List user's bots
    bots = user_bots.get(user_id, [])
    if not bots:
        bot.send_message(chat_id, "😕 You haven't created any bots yet.")
    else:
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        markup.row("🔙 Back to Menu")
        for botname in bots:
            markup.row(f"🗑 Delete {botname}")
        bot.send_message(chat_id, "🤖 Your Bots:", reply_markup=markup)

elif text.startswith("🗑 Delete"):
    # Delete selected bot
    botname = text.split("🗑 Delete ")[-1].strip()
    if user_id in user_bots and botname in user_bots[user_id]:
        user_bots[user_id].remove(botname)
        bot.send_message(chat_id, f"✅ {botname} has been deleted.")
    else:
        bot.send_message(chat_id, "❌ Bot not found.")

elif text == "🛠️ Tools":
    bot.send_message(chat_id, "🔧 Tools:\n1️⃣ Remove Forward Tag ➡ @forwardtag0bot")

elif text == "📢 Promotion":
    bot.send_message(chat_id, "📢 Free Promotion Available!\nDM @DARKN8002 with proof of funds to get started.")

elif text == "🔙 Back to Menu":
    # Go back to main menu
    menu = types.ReplyKeyboardMarkup(resize_keyboard=True)
    menu.row("📦 Create Bot", "🤖 My Bots")
    menu.row("🛠️ Tools", "📢 Promotion", "🗑 Delete Bot")
    bot.send_message(chat_id, "👋 Back to main menu:", reply_markup=menu)

# Template selection buttons

@bot.callback_query_handler(func=lambda call: call.data.startswith('template_')) def handle_template_choice(call): user_id = call.from_user.id chat_id = call.message.chat.id

# Ask for API token after template selection
bot.send_message(chat_id, "🧾 Get your API token from @BotFather and send it here:")
bot.register_next_step_handler(call.message, handle_token_submission)

# Handle API token submission

def handle_token_submission(message): token = message.text.strip() user_id = message.from_user.id chat_id = message.chat.id

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

    if bot_username in user_bots[user_id]:
        bot.send_message(chat_id, f"⚠️ Bot {bot_username} already exists. Send /adminaccess in your bot to continue editing.")
        return

    user_bots[user_id].append(bot_username)

    # Send bot success message
    bot.send_message(chat_id, f"✅ Bot created: {bot_username}\nSend /adminaccess in your bot to continue setup.")

except Exception as e:
    bot.send_message(chat_id, f"❌ Error: {str(e)}")

# Show template menu with view buttons

def template_menu(): markup = types.InlineKeyboardMarkup(row_width=2) markup.row( types.InlineKeyboardButton("🎨 Template 1", callback_data='template_1'), types.InlineKeyboardButton("🔍 View", url="https://example.com/template1") ) markup.row( types.InlineKeyboardButton("🎨 Template 2", callback_data='template_2'), types.InlineKeyboardButton("🔍 View", url="https://example.com/template2") ) markup.row( types.InlineKeyboardButton("🎨 Template 3", callback_data='template_3'), types.InlineKeyboardButton("🔍 View", url="https://example.com/template3") ) markup.row( types.InlineKeyboardButton("🎨 Template 4", callback_data='template_4'), types.InlineKeyboardButton("🔍 View", url="https://example.com/template4") ) return markup

Start polling the bot

bot.infinity_polling()

