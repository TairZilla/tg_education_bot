import os
import learning
from dotenv import load_dotenv

#Извлечение переменных окружения
dotenv_path = os.path.join(os.path.dirname(__file__),'..', '.env')
if os.path.exists(dotenv_path):
    load_dotenv(dotenv_path)

BOT_TOKEN = os.getenv('BOT_TOKEN')
ADMIN = os.getenv('ADMIN')

#Здесь можно изменить список предметов
__sub_list = ['Алгебра', 'Физика', 'Геометрия']

ALGEBRA_TOPICS = [
        "Линейные уравнения с одной переменной", 
        "Тождества",
        "Степени",
        "Одночлены",
        "Многочлены",
        "Функции",
        "Системы линейных уравнений с двумя переменными"
    ]

MANAGE_DICT = {
    "алгебра" : learning.ALGEBRA_DATA,
    "физика" : learning.PHYSICS_DATA,
    "геометрия" : learning.GEOMITRY_DATA
}

GEOMETRY_TOPICS = [
    "Основные геометрические понятия",
    "Параллельные линии",
    "Углы"
]

PHYSICS_TOPICS = [
    "Введение в физику",
    "Скорость и ускорение",
    "Сила тяжести"
]

SUBJECT_LIST = [item.lower() for item in __sub_list]

#Здесь можно изменить надпись на кнопке отмены
CANCEL_WORD = 'отмена'

#Спец. символы которые вырезаются из поискового запроса.
SPECIAL_SYMBOLS = [".", ",", "!", "?", "@", "#", "$", "%", "^", "&", "*", "(", ")", "-", "_", "+", "=", "[", "]", "{", "}", ";", ":", "'", '"', "<", ">", "/", "\\"]
