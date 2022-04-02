import os


import telebot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton


from dotenv import load_dotenv

load_dotenv()

TOKEN = os.environ["TOKEN"]
PHOTO_ID = os.environ["PHOTO_ID"]
CHANNEL = os.environ["CHANNEL"]

bot = telebot.TeleBot(TOKEN)


# Heleper functions
def get_start_markup():
    markup = InlineKeyboardMarkup()
    markup.row_width = 1
    markup.add(InlineKeyboardButton("Start", callback_data="start"))
    return markup


def get_next_markup():
    markup = InlineKeyboardMarkup()
    markup.row_width = 1
    markup.add(
        InlineKeyboardButton(
            "Buy TEDx Ticket",
            url="http://campus.covenantuniversity.edu.ng/tedxcovenant-university",
        ),
        InlineKeyboardButton("Call Support", url="https://t.me/favournelson"),
    )
    return markup


@bot.message_handler(commands=["start"], chat_types=["private"])
def start(message):
    bot.send_photo(
        message.chat.id,
        caption="Welcome to Covenant University TEDx Community",
        photo=PHOTO_ID,
        reply_markup=get_start_markup(),
    )


@bot.callback_query_handler(func=lambda call: True)
def start_query_handler(call):
    # Check if a start command was sent, if not skip
    if call.data != "start":
        return

    # Initialise variables
    user_id = call.from_user.id
    chat_id = call.message.chat.id

    # Check if user is a member of TEDx Channel, if not, end function execution
    if bot.get_chat_member(CHANNEL, user_id=user_id).status == "left":
        bot.send_message(
            chat_id,
            text="You're not a member of the channel⁉\n\
You need to join the [TEDxCovenantUniversity Channel](https://t.me/tedxcovenantuniversity)",
            parse_mode="MarkdownV2",
        )

        bot.send_message(
            chat_id,
            text="I have joined the channel",
            reply_markup=get_start_markup(),
        )
        return

    else:
        bot.send_message(
            chat_id,
            text="✅Thank you for joining the \
TEDxCovenantUniversity Community",
            parse_mode="MarkdownV2",
            reply_markup=get_next_markup(),
        )


bot.infinity_polling()
