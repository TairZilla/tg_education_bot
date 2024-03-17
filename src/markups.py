from telebot import types
import settings

def get_menu_markup() -> types.ReplyKeyboardMarkup:
    markup = types.ReplyKeyboardMarkup(row_width=3, resize_keyboard=True)

    for subject in settings.SUBJECT_LIST:
        markup.add(
            types.KeyboardButton(subject.lower().capitalize())
        )
    return markup

def get_cancel_markup() -> types.ReplyKeyboardMarkup:
    markup = types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
    markup.add(
            types.KeyboardButton(settings.CANCEL_WORD.lower().capitalize())
        )
    return markup

def get_empty_markup() -> types.ReplyKeyboardMarkup:
    return types.ReplyKeyboardRemove(selective=True)

def get_topics_markup(topics: list) -> types.ReplyKeyboardMarkup:
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    while topics:
        row = [types.KeyboardButton(topic) for topic in topics[:2]]
        markup.row(*row)
        topics = topics[2:]
    return markup