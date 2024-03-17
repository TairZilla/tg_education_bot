import sqlite3, os

# Указываем путь до места где храниться наша база данных
DB_PATH = os.path.join(os.path.dirname(__file__),'..', 'bot.db')

# Функция создания таблицы - создаёт таблицу в базе данных с 3 полями: ID, username и user_id
def create_table():
    try:
        connection = sqlite3.connect(DB_PATH)
        cursor = connection.cursor()

        create_table_query = '''
            CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL,
            user_id INTEGER NOT NULL
        );
        '''

        cursor.execute(create_table_query)
        connection.commit()
        
    finally:
        connection.close()

# Функция по удалению базы данных
def drop_table():
    try:
        connection = sqlite3.connect(DB_PATH)
        cursor = connection.cursor()
        drop_table_query = f'DROP TABLE IF EXISTS users;'
        cursor.execute(drop_table_query)
        connection.commit()
    finally:
        connection.close()

# Функция, которая добавляет пользователя в базу данных
def insert_user(username:str, user_id:int):
    try:
        connection = sqlite3.connect(DB_PATH)
        cursor = connection.cursor()

        # Проверяем, существует ли пользователь с указанным user_id
        select_query = f'''
        SELECT * FROM users
        WHERE user_id = ?;
        '''
        values = (user_id,)
        cursor.execute(select_query, values)

        existing_user = cursor.fetchone()
        if not existing_user:
            insert_query = f'''INSERT INTO users (username, user_id) VALUES (?, ?);'''
            values = (username, user_id)
            cursor.execute(insert_query, values)
            connection.commit()
    finally:
        connection.close()

# Функция для составления списка пользователей из базы данных и отправки в бот админу
def get_users():
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        select_query = f'''
        SELECT * FROM users;
        '''
        cursor.execute(select_query)
        user_data = cursor.fetchall()
        results = []
        if user_data:
            for user in user_data:
                
                user_info = {
                    'id': user[0],
                    'username': user[1],
                    'user_id': user[2]
                }
                results.append(user_info)

            return results
    finally:
        conn.close()

# Функция получения пользователя по его id (На данный момент не используем)
# def get_user_by_id(user_id):
#     try:
#         conn = sqlite3.connect(DB_PATH)
#         cursor = conn.cursor()
#         select_query = f'''
#         SELECT * FROM users
#         WHERE user_id = ?;
#         '''
#         values = (user_id,)
#         cursor.execute(select_query, values)
#         user_data = cursor.fetchone()

#         if user_data:
#             user_info = {
#                 'id': user_data[0],
#                 'username': user_data[1],
#                 'user_id': user_data[2]
#             }
#             return user_info
#         else:
#             print(f"Пользователь с user_id {user_id} не найден.")
#     finally:
#         conn.close()

if __name__ == '__main__':
    drop_table()
    create_table()