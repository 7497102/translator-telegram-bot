from telebot.types import ReplyKeyboardMarkup, KeyboardButton

from configs import LANGUAGES

def generate_langs():
    markup = ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
    buttons = []
    for value in LANGUAGES.values():
        btn = KeyboardButton(text=value)
        buttons.append(btn)

    markup.add(*buttons)
    return markup