import logging
from telebot import TeleBot, types

import settings
import messages
import db
import markups
import handler

# Настройка логирования
logging.basicConfig(level=logging.INFO)

bot = TeleBot(token=settings.BOT_TOKEN)

def send_message(chat_id: int, text: str, reply_markup=None):
    """Универсальная функция для отправки сообщений."""
    if reply_markup is None:
        reply_markup = markups.get_empty_markup()
    bot.send_message(chat_id=chat_id, text=text, reply_markup=reply_markup)

def is_admin(user_id: int) -> bool:
    """Проверяет, является ли пользователь администратором."""
    return str(user_id) == settings.ADMIN

@bot.message_handler(commands=['start'])
def handle_start(message: types.Message):
    send_message(
        chat_id=message.chat.id,
        text=messages.MESSAGE_HELLO
    )
    db.insert_user(message.from_user.username, message.from_user.id)

@bot.message_handler(commands=['1001'])
def handle_creepy(message: types.Message):
    send_message(
        chat_id=message.chat.id,
        text=messages.ERROR_1001
    )

@bot.message_handler(commands=['bye_bye'])
def handle_bye_bye(message: types.Message):
    send_message(
        chat_id=message.chat.id,
        text=messages.BYE_BYE
    )

@bot.message_handler(commands=['info'])
def handle_info(message: types.Message):
    send_message(
        chat_id=message.chat.id,
        text=messages.MESSAGE_INFO
    )

@bot.message_handler(commands=['cancel'])
def handle_cancel(message: types.Message):
    send_message(
        chat_id=message.chat.id,
        text=messages.MESSAGE_CANCEL
    )

@bot.message_handler(commands=['admin'])
def handle_admin(message: types.Message):
    if is_admin(message.from_user.id):
        users = db.get_users()
        data = [f'{item["id"]} {item["username"]} {item["user_id"]}' for item in users]
        send_message(
            chat_id=message.chat.id,
            text='\n'.join(data)
        )
    else:
        send_message(
            chat_id=message.chat.id,
            text=messages.CANCEL_ID
        )

@bot.message_handler(commands=['menu'])
def handle_menu(message: types.Message):
    send_message(
        chat_id=message.chat.id,
        text=messages.MESSAGE_MENU,
        reply_markup=markups.get_menu_markup()
    )
    bot.register_next_step_handler(message, subject_choice)

def subject_choice(message: types.Message):
    if message.text == '/cancel':
        send_message(
            chat_id=message.chat.id,
            text=messages.MESSAGE_CANCEL
        )
        return

    choice = message.text.lower()
    subjects = {
        "алгебра": settings.ALGEBRA_TOPICS,
        "физика": settings.PHYSICS_TOPICS,
        "геометрия": settings.GEOMETRY_TOPICS
    }

    if choice in subjects:
        send_message(
            chat_id=message.chat.id,
            text=f"Выберите тему по {choice}:",
            reply_markup=markups.get_topics_markup(subjects[choice])
        )
        bot.register_next_step_handler(message, topic_choice, choice)
    else:
        send_message(
            chat_id=message.chat.id,
            text=messages.MESSAGE_CHOICE_SUBJECT_ERROR,
            reply_markup=markups.get_menu_markup()
        )
        bot.register_next_step_handler(message, subject_choice)

def topic_choice(message: types.Message, subject: str):
    if message.text == '/cancel':
        send_message(
            chat_id=message.chat.id,
            text=messages.MESSAGE_CANCEL
        )
        return

    topic = message.text
    valid_topics = settings.MANAGE_DICT.get(subject, {})

    if topic in valid_topics:
        send_message(
            chat_id=message.chat.id,
            text=messages.MESSAGE_CHOICE.format(
                choice=subject.capitalize(),
                topic=topic.capitalize()
            )
        )
        bot.register_next_step_handler(message, search, subject, topic)
    else:
        send_message(
            chat_id=message.chat.id,
            text='Воспользуйтесь клавиатурой для выбора темы ^_^',
            reply_markup=markups.get_topics_markup(valid_topics.keys())
        )
        bot.register_next_step_handler(message, topic_choice, subject)

def search(message: types.Message, subject: str, topic: str):
    if message.text == '/cancel':
        send_message(
            chat_id=message.chat.id,
            text=messages.MESSAGE_CANCEL
        )
        return

    query = message.text.lower()
    for symbol in settings.SPECIAL_SYMBOLS:
        query = query.replace(symbol, '')

    keywords = query.split()
    data = settings.MANAGE_DICT.get(subject, {}).get(topic, {})

    if data and len(keywords) >= 2:
        response = handler.find_in_dict(
            border=len(keywords),
            keywords=keywords,
            data=data
        )
        if response:
            send_message(
                chat_id=message.chat.id,
                text=messages.MESSAGE_200
            )
            for item in response:
                content = data
                for key in item.split('|'):
                    content = content.get(key, {})
                message_text = content
                if '&graph&' in message_text:
                    message_text = message_text.replace('&graph&', '')
                    send_message(
                        chat_id=message.chat.id,
                        text=message_text
                    )
                    with open('./media/img/a.jpg', 'rb') as file:
                        bot.send_photo(
                            message.chat.id,
                            photo=file
                        )
                else:
                    send_message(
                        chat_id=message.chat.id,
                        text=message_text
                    )
        else:
            send_message(
                chat_id=message.chat.id,
                text=messages.MESSAGE_404
            )
            send_message(
                chat_id=message.chat.id,
                text='Попробуйте ввести запрос ещё раз или смените тему, используя /cancel'
            )
            bot.register_next_step_handler(message, search, subject, topic)
    else:
        send_message(
            chat_id=message.chat.id,
            text=messages.MESSAGE_403
        )

@bot.message_handler(content_types=['text'])
def handle_all_messages(message: types.Message):
    send_message(
        chat_id=message.chat.id,
        text=messages.MESSAGE_ALWAYS_CAME_BACK
    )

if __name__ == "__main__":
    logging.info('Бот запущен')
    bot.infinity_polling()