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
        InlineKeyboardButton(
            "Buy TEDx Ticket",
            url="http://campus.covenantuniversity.edu.ng/tedxcovenant-university",
        ),
        InlineKeyboardButton("Call Support", url="https://t.me/favournelson"),
        InlineKeyboardButton("Get personalised Link", callback_data="link"),
    )
    return markup
