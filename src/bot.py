from telebot import TeleBot, types

import settings, messages, db, markups, handler

bot = TeleBot(token=settings.BOT_TOKEN)


@bot.message_handler(commands=['start'])
def start_message(message:types.Message):
    bot.send_message(
        chat_id=message.chat.id,
        text=messages.MESSAGE_HELLO,
    )
    db.insert_user(message.from_user.username, message.from_user.id)

@bot.message_handler(commands=['menu'])
def menu_message(message:types.Message):
    bot.send_message(
        chat_id=message.chat.id,
        text=messages.MESSAGE_MENU,
        reply_markup=markups.get_menu_markup()
    )
    bot.register_next_step_handler(message, subject_choice)


def subject_choice(message:types.Message):
    choice = message.text.lower()
    if choice in settings.SUBJECT_LIST:
        bot.send_message(
            chat_id = message.chat.id,
            text = messages.MESSAGE_CHOICE.format(choice=choice),
            reply_markup = markups.get_empty_markup()
        )
        bot.register_next_step_handler(message, search, choice)
    else:
        bot.send_message(
            chat_id=message.chat.id,
            text=messages.MESSAGE_CHOICE_SUBJECT_ERROR,
            reply_markup=markups.get_menu_markup(need_cancel=True)
        )
        bot.register_next_step_handler(message, subject_choice)


def search(message:types.Message, choice):
    search_str = message.text.lower()

    if search_str == settings.CANCEL_WORD:
        bot.send_message(message.chat.id, text=messages.MESSAGE_CANCEL, reply_markup=markups.get_empty_markup())
        return
    for symbol in settings.SPECIAL_SYMBOLS:
        search_str = search_str.replace(symbol,'')

    search_str = search_str.split(" ")
    response = handler.search_in_json(*search_str)

    bot.send_message(message.chat.id, text='\n'.join(response), reply_markup=markups.get_cancel_markup())

    bot.register_next_step_handler(message, search, choice)

if __name__ == "__main__":
        bot.infinity_polling()