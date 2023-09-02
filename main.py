from telebot import TeleBot
from telebot.types import Message
from keyboards import generate_langs
from googletrans import Translator
from telebot.types import ReplyKeyboardRemove
from queries import insert_translate_history, select_history

bot = TeleBot('5747673023:AAFBSQgDroXIkMCRZ7MO9e1hwZWvMkpNLX4')

@bot.message_handler(commands=['start', 'history', 'about_dev'])
def commands(message: Message):
  if message.text == '/start':
      full_name = message.from_user.full_name
      user_id = message.from_user.id
      bot.send_message(user_id, f"""Hello {full_name}!!! I'm Naruto dattebayo 🖖🏼""")
      bot.send_sticker(user_id, 'CAACAgIAAxkBAAEGEMBjRpyVdOsrG-6fxMfNVTT5sdpjVAACrw0AAk2yoUvsGprXoh3YWioE')
      ask_first_language(message)
  elif message.text == '/history':
      show_history(message)
  elif message.text == '/about_dev':
      user_id = message.from_user.id
      bot.send_message(user_id, f"""This bot created by t.me/Jaf_Hanma""")
      ask_first_language(message)


def show_history(message: Message):
    user_id = message.from_user.id
    translates = select_history(user_id)

    for tg in translates[:-6:-1]:
        bot.send_message(user_id, f"""
From Language: {tg[0]}
To language: {tg[1]}
Original text: {tg[2]}
Translated text: {tg[3]}
""")
        ask_first_language(message)

def ask_first_language(message: Message):
    user_id = message.from_user.id
    mss = bot.send_message(user_id, f"""Please choose from which language do you want to translate:""",
                     reply_markup=generate_langs())
    bot.register_next_step_handler(mss, ask_second_language)

def ask_second_language(message: Message):
    if message.text in ['/start', '/history', '/about_dev']:
        commands(message)
    else:
        user_id = message.from_user.id
        first_language = message.text
        mss = bot.send_message(user_id, f"""Please choose to which language do you want to translate:""",
                                   reply_markup=generate_langs())
        bot.register_next_step_handler(mss, ask_text, first_language)

def ask_text(message: Message, first_language):
    if message.text in ['/start', '/history', '/about_dev']:
        commands(message)
    else:
        user_id = message.from_user.id
        second_language = message.text
        mss = bot.send_message(user_id, f"""Please, send me text/word you want to translate:""",
                               reply_markup=ReplyKeyboardRemove())

        bot.register_next_step_handler(mss, translate, first_language, second_language)

def translate(message: Message, first_language, second_language):
    if message.text in ['/start', '/history', '/about_dev']:
        commands(message)
    else:
        user_id = message.from_user.id
        org_text = message.text
        translator = Translator()
        translated_text = translator.translate(src=first_language.split(' ')[0],
                                               dest=second_language.split(' ')[0],
                                               text=org_text).text
        bot.send_message(user_id, translated_text)

        insert_translate_history(telegram_id=user_id,
                                 src=first_language,
                                 dest=second_language,
                                 org_text=org_text,
                                 tr_text=translated_text)




bot.polling(none_stop=True)
