import os

from flask import Flask, request

import telebot

from app import markups, mongo

from dotenv import load_dotenv

load_dotenv()

TOKEN = os.environ["TOKEN"]
PHOTO_ID = os.environ["PHOTO_ID"]
CHANNEL = os.environ["CHANNEL"]
ADMIN = os.environ["ADMIN"]

bot = telebot.TeleBot(TOKEN)
server = Flask(__name__)


@bot.message_handler(commands=["start"], chat_types=["private"])
def start(message):
    """
    Handle start messages
    """
    user = message.from_user
    mongo.insert_new_user(
        id=user.id,
        username=user.username,
        first_name=user.first_name,
        last_name=user.last_name,
    )

    message_text_list = message.text.split(" ")
    users_firstname = message.from_user.first_name.split(" ")[0]

    # Updates referal if the start message is more than length of 1 string
    if len(message_text_list) > 1:
        mongo.update_referral(message_text_list[-1], message.from_user.id)

    bot.send_photo(
        message.chat.id,
        caption=f"Hi {users_firstname.title()},  My name is Alex 👨‍✈️, the TEDxbot, and I am here to make your experience memorable.",
        photo=PHOTO_ID,
        reply_markup=markups.get_start_markup(),
    )


@bot.callback_query_handler(func=lambda call: call.data == "start")
def start_query_handler(call):
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
            reply_markup=markups.get_start_markup(),
        )
        return

    else:
        bot.send_message(
            chat_id,
            text="✅Thank you for joining the \
TEDxCovenantUniversity Community",
            parse_mode="MarkdownV2",
            reply_markup=markups.get_next_markup(),
        )


@bot.callback_query_handler(func=lambda call: call.data == "link")
def get_referral_link(call):
    # Creates a referral link for the user and adds them as a participant

    user = call.from_user
    chat = call.message.chat
    link_caption = (
        "You can share this link with your friends and win some amazing prizes🤑\n"
    )

    # Checks if user has a telegram usename
    if not user.username:
        bot.send_message(
            chat.id,
            text=f"{link_caption}\nhttps://t.me/tedxcu_bot/?start=_0_{user.id}_",
        )
    else:
        bot.send_message(
            chat.id,
            text=f"{link_caption}\nhttps://t.me/tedxcu_bot/?start=_{user.username}_0_{user.id}_",
        )

    mongo.insert_new_participant(
        id=user.id,
        username=user.username,
        first_name=user.first_name,
        last_name=user.last_name,
    )


@bot.message_handler(func=lambda message: message.from_user.id == int(ADMIN))
def broadcast_message(message):
    """
    Brodcasts messages from admin to all bot users
    """
    user_ids = mongo.get_ids()
    for user_id in user_ids:
        bot.send_message(user_id, text=message.text)


@server.route("/" + TOKEN, methods=["POST"])
def getMessage():
    json_string = request.get_data().decode("utf-8")
    update = telebot.types.Update.de_json(json_string)
    bot.process_new_updates([update])
    return "!", 200


@server.route("/")
def webhook():
    bot.remove_webhook()
    bot.set_webhook(url="https://tedx-cu-bot.herokuapp.com/" + TOKEN)
    return "!", 200


if __name__ == "__main__":
    server.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
