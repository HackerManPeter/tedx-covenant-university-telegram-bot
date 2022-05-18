import os
import time
from typing import List


import telebot

try:
    from app import markups, mongo
except:
    import markups, mongo

from dotenv import load_dotenv

load_dotenv()

TOKEN = os.environ["TOKEN2"]
PHOTO_ID = os.environ["PHOTO_ID2"]
CHANNEL = os.environ["CHANNEL2"]
ADMIN = os.environ["ADMIN"]
AGS = int(os.environ["AGS"])

bot = telebot.TeleBot(TOKEN)

def send_messages(ids: List[str], func, **kwargs):
    count = 0
    for id in ids:
        try:
            func(id, **kwargs)
            count += 1
        except:
            continue
        if count % 20 == 0:
            time.sleep(.7)


@bot.message_handler(commands=["start"], chat_types=["private"])
def start(message):
    """
    Handle start messages
    """
    user = message.from_user
    if user.id == int(AGS):
        message = '''Hi Admin, any messsage you send to the bot would be broadcast to all users

Example
```
/sendphoto
I am the tedx Bot
```

This would send the a photo with the caption "I am the tedx Bot" to all abot users

Any message sent to the bot that is not a /start message would be broadcast to all users
'''
        bot.send_message(user.id, text=message, parse_mode='MarkdownV2')
        return

    # Add new user to the broadcasting database
    mongo.insert_new_user(
        id=user.id,
        username=user.username,
        first_name=user.first_name,
        last_name=user.last_name,
    )

    message_text_list = message.text.split(" ")
    users_firstname = user.first_name.split(" ")[0]

    # Updates referal if the start message is more than length of 1 string
    if len(message_text_list) > 1:
        mongo.update_referral(message_text_list[-1], user.id)

    # Reply /start message
    bot.send_photo(
        message.chat.id,
        caption=f"Hi {users_firstname.title()},  My name is Alex 👨‍✈️, the TEDxbot, and I am here to make your experience memorable.",
        photo=PHOTO_ID,
        reply_markup=markups.get_start_markup(),
    )


@bot.callback_query_handler(func=lambda call: call.data == "start")
def start_query_handler(call):
    """
    Handle the "start" Callback query
    """
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


@bot.message_handler(func=lambda message: message.text.startswith("/sendphoto"))
def broadcast_image(message):
    """
    Handles messages with meant for image captions
    """
    # Check if User is admin
    if message.from_user.id != int(AGS):
        return

    # Remove "/sendphoto" from message.text
    caption = "\n".join(message.text.split("\n")[1:])

    # Broadcast image with message.text as caption
    image_id = mongo.get_image_id()

    user_ids = [
        AGS,
    ]
    send_messages(user_ids, func=bot.send_photo, photo=image_id, caption=caption)


@bot.message_handler(func=lambda message: message.from_user.id == int(AGS))
def broadcast_message(message):
    """
    Brodcasts messages from admin to all bot users
    """
    user_ids = [
        AGS,
    ]
    send_messages(user_ids, func=bot.send_message, text=message.text)


@bot.message_handler(content_types=["photo"])
def save_image(message):
    """
    Get's image ID from message and upload to Mongo
    """
    if message.from_user.id != int(AGS):
        return
    image_id = message.photo[0].file_id
    mongo.change_image_id(image_id)

if __name__ == "__main__":
    bot.infinity_polling()  