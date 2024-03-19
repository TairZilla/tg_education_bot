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
    
@bot.message_handler(commands=['1001'])
def creepy_message(message:types.Message):
    bot.send_message(
        chat_id = message.chat.id,
        text = messages.ERROR_1001,
        reply_markup = markups.get_empty_markup()
    )

@bot.message_handler(commands = ["bye_bye"])
def miuning(message: types.Message):
    bot.send_message(
        chat_id = message.chat.id,
        text = messages.BYE_BYE,
        reply_markup = markups.get_empty_markup()
    )

@bot.message_handler(commands=['info'])
def info_message(message:types.Message):
    bot.send_message(
        chat_id=message.chat.id,
        text=messages.MESSAGE_INFO,
    )

@bot.message_handler(commands=['cancel'])
def cancel_message(message:types.Message):
    bot.send_message(
        chat_id=message.chat.id,
        text=messages.MESSAGE_CANCEL,
        reply_markup=markups.get_empty_markup()
    )

@bot.message_handler(commands=['admin'])
def admin_message(message:types.Message):
    admin = message.from_user.id
    if str(admin) == settings.ADMIN:
        data = [f'{item["id"]} {item["username"]} {item["user_id"]}' for item in db.get_users()]
        bot.send_message(
            chat_id = message.chat.id,
            text = '\n'.join(data),
            reply_markup = markups.get_empty_markup()
        )
    else:
        bot.send_message(
            chat_id = message.chat.id,
            text = messages.CANCEL_ID,
            reply_markup = markups.get_empty_markup()
        )

@bot.message_handler(commands=['menu'])
def menu_message(message:types.Message):
    bot.send_message(
        chat_id=message.chat.id,
        text=messages.MESSAGE_MENU,
        reply_markup=markups.get_menu_markup()
    )
    bot.register_next_step_handler(message, subject_choice)

def subject_choice(message:types.Message):
    if message.text == '/cancel':
        bot.send_message(
            chat_id=message.chat.id, 
            text=messages.MESSAGE_CANCEL, 
            reply_markup=markups.get_empty_markup())
        return 
    choice = message.text.lower()
    if choice == "алгебра":
        bot.send_message(
            chat_id=message.chat.id,
            text="Выберите тему по алгебре:",
            reply_markup=markups.get_topics_markup(settings.ALGEBRA_TOPICS)
        )
        bot.register_next_step_handler(message, topic_choice, choice)
    elif choice == "физика":
        bot.send_message(
            chat_id=message.chat.id,
            text="Выберите тему по физике:",
            reply_markup=markups.get_topics_markup(settings.PHYSICS_TOPICS)
        )
        bot.register_next_step_handler(message, topic_choice, choice)
    elif choice == "геометрия":
        bot.send_message(
            chat_id=message.chat.id,
            text="Выберите тему по геометрии:",
            reply_markup=markups.get_topics_markup(settings.GEOMETRY_TOPICS)
        )
        bot.register_next_step_handler(message, topic_choice, choice)
    else:
        bot.send_message(
            chat_id=message.chat.id,
            text=messages.MESSAGE_CHOICE_SUBJECT_ERROR,
            reply_markup=markups.get_menu_markup()
        )
        bot.register_next_step_handler(message, subject_choice)


def topic_choice(message:types.Message, choice:str):
    if message.text == '/cancel':
        bot.send_message(
            chat_id=message.chat.id, 
            text=messages.MESSAGE_CANCEL, 
            reply_markup=markups.get_empty_markup())
        return
    topic = message.text

    if topic in settings.ALGEBRA_TOPICS or topic in settings.GEOMETRY_TOPICS or topic in settings.PHYSICS_TOPICS:

        bot.send_message(
            message.chat.id,
            text=messages.MESSAGE_CHOICE.format(
                choice = choice.lower().capitalize(),
                topic = topic.lower().capitalize()
            ),
            reply_markup=markups.get_empty_markup()
        )
        bot.register_next_step_handler(message, search, choice, topic)
    else:
        bot.send_message(
            message.chat.id,
            text = 'Воспользуйся клавиатурой для того чтобы выбрать тему по предмету ^_^',
            reply_markup = markups.get_topics_markup()
        )
        bot.register_next_step_handler(message, topic_choice, choice)
    
def search(message:types.Message, choice, topic):
    if message.text == '/cancel':
        bot.send_message(chat_id=message.chat.id, text=messages.MESSAGE_CANCEL, reply_markup=markups.get_empty_markup())
        return
    
    topic_choice_str = message.text.lower()

    for symbol in settings.SPECIAL_SYMBOLS:
        topic_choice_str = topic_choice_str.replace(symbol,'')

    topic_choice_str = topic_choice_str.split(" ")
    
    if topic in settings.MANAGE_DICT[choice].keys() and len(topic_choice_str) >= 2 and choice in settings.MANAGE_DICT.keys():
        response = handler.find_in_dict(
            border=len(topic_choice_str),
            keywords=topic_choice_str,
            data=settings.MANAGE_DICT[choice][topic]
        )
        if response:
            bot.send_message(
                message.chat.id,
                text=messages.MESSAGE_200,
                reply_markup=markups.get_empty_markup()
            )
            for item in response:
                data = settings.MANAGE_DICT[choice][topic]
                for part_path in item.split('|'):
                    data = data.get(part_path)
                to_mes = data
                if '&graph&' in to_mes:
                    
                    bot.send_message(
                        message.chat.id,
                        text=to_mes.replace('&graph&', ''),
                        reply_markup=markups.get_empty_markup()
                    )
                    with open ('/media/img/a.jpg', 'rb') as file:
                        bot.send_photo(
                            message.chat.id,
                            photo=file
                        )
                else:
                    bot.send_message(
                        message.chat.id,
                        text=to_mes,
                        reply_markup=markups.get_empty_markup()
                    )
        else:
            bot.send_message(
                message.chat.id,
                text=messages.MESSAGE_404,
                reply_markup=markups.get_empty_markup()
            )
            bot.send_message(
                message.chat.id,
                text = 'Попробуй ввести свой запрос ещё раз или поменяй тему используя /cancel',
                reply_markup = markups.get_empty_markup()
            )
    else:
        bot.send_message(
            message.chat.id,
            text=messages.MESSAGE_403,
            reply_markup=markups.get_empty_markup()
        )

    bot.register_next_step_handler(message, search, choice, topic),

@bot.message_handler(content_types=['text'])
def message_all(message:types.Message):
    bot.send_message(
        chat_id = message.chat.id,
        text = messages.MESSAGE_ALWAYS_CAME_BACK,
        reply_markup = markups.get_empty_markup()
    )

if __name__ == "__main__":
        print('Бот запустился')
        bot.infinity_polling()