import os

from dotenv import load_dotenv

from telebot.types import InlineKeyboardButton, InlineKeyboardMarkup

load_dotenv()


def get_start_markup():
    """
    Start markup
    """
    markup = InlineKeyboardMarkup()
    markup.row_width = 1
    markup.add(InlineKeyboardButton("Start", callback_data="start"))
    return markup


def get_next_markup():
    """
    Adds Markup for Bot functions
    """
    markup = InlineKeyboardMarkup()
    markup.row_width = 1
    markup.add(
        # InlineKeyboardButton(
        #     "Buy TEDx Ticket 🎟",
        #     url="https://flutterwave.com/pay/tedxcovenantuniversitytickets",
        # ),
        # InlineKeyboardButton(
        #     "Buy your TEDx merch 🧣🕶️",
        #     url="https://flutterwave.com/store/custudentcouncil/lth6m3fpfqbw",
        # ),
        InlineKeyboardButton(
            "Buy TEDx Ticket 🎟",
            url="https://flutterwave.com/store/custudentcouncil/lth6m3fpfqbw",
        ),
        InlineKeyboardButton(
            "Connect with us 🔗", url="https://bit.ly/TEDxCovenantUniversity2022"
        ),
        InlineKeyboardButton("Contact Support 👩‍💻", url="https://t.me/mofope_a"),
        InlineKeyboardButton("Get referral Link 🖇", callback_data="link"),
    )
    return markup
