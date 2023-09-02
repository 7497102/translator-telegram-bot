user_id = message.from_user.id
full_name = message.from_user.full_name
bot.send_message(user_id, f"""Hello {full_name}!!! I'm Naruto dattebayo 🖖🏼""")
bot.send_sticker(user_id, 'CAACAgIAAxkBAAEGEMBjRpyVdOsrG-6fxMfNVTT5sdpjVAACrw0AAk2yoUvsGprXoh3YWioE')