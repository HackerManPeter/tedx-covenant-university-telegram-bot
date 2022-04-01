import os

from dotenv import load_dotenv

from telebot import TeleBot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton


load_dotenv()
TOKEN = os.environ["TOKEN"]
CHANNEL = os.environ["CHANNEL"]

bot = TeleBot("TOKEN")


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
