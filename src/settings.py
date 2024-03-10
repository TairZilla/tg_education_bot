import os
from dotenv import load_dotenv

#Извлечение переменных окружения
dotenv_path = os.path.join(os.path.dirname(__file__),'..', '.env')
if os.path.exists(dotenv_path):
    load_dotenv(dotenv_path)

BOT_TOKEN = os.getenv('BOT_TOKEN')

#Здесь можно изменить список предметов
__sub_list = ['Алгебра', 'Физика', 'Геометрия']

SUBJECT_LIST = [item.lower() for item in __sub_list]

#Здесь можно изменить надпись на кнопке отмены
CANCEL_WORD = 'отмена'

#Спец. символы которые вырезаются из поискового запроса.
SPECIAL_SYMBOLS = [".", ",", "!", "?", "@", "#", "$", "%", "^", "&", "*", "(", ")", "-", "_", "+", "=", "[", "]", "{", "}", ";", ":", "'", '"', "<", ">", "/", "\\"]





