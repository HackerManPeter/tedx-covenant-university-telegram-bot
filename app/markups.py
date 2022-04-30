import os

from dotenv import load_dotenv

from telebot.types import InlineKeyboardButton, InlineKeyboardMarkup

load_dotenv()


def get_start_markup() -> InlineKeyboardMarkup:
    """
    Start markup
    """
    markup = InlineKeyboardMarkup()
    markup.row_width = 1
    markup.add(InlineKeyboardButton("Start", callback_data="start"))
    return markup


def get_next_markup() -> InlineKeyboardMarkup:
    """
    Adds Markup for Bot functions
    """
    markup = InlineKeyboardMarkup()
    markup.row_width = 1
    markup.add(
        InlineKeyboardButton(
            "Buy your TEDx merch 🧣🕶️",
            url="https://flutterwave.com/store/custudentcouncil/lth6m3fpfqbw",
        ),
        InlineKeyboardButton(
            "Buy TEDx Ticket 🎟",
            url="https://flutterwave.com/pay/60mayht7ffdm",
        ),
        InlineKeyboardButton(
            "Connect with us 🔗", url="https://bit.ly/TEDxCovenantUniversity2022"
        ),
        InlineKeyboardButton("Contact Support 👩‍💻", url="https://t.me/mofope_a"),
        InlineKeyboardButton("Get referral Link 🖇", callback_data="link"),
    )
    return markup
