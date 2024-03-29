import sqlite3


class BotDB:
    def __init__(self, db_file):
        self.conn = sqlite3.connect(db_file)
        self.cursor = self.conn.cursor()

    # Проверка пользователя в базе данных
    def user_exists(self, user_id):
        result = self.cursor.execute("SELECT id FROM records WHERE user_id = ? ", (user_id,))
        return bool(len(result.fetchall()))

    # Добавление пользователя в базу данных
    def add_user(self, user_id):
        self.cursor.execute("INSERT INTO records (user_id) VALUES (?)", (user_id,))
        return self.conn.commit()

    # Получение id пользователя в базе данных
    def get_user_id(self, user_id):
        result = self.cursor.execute("SELECT id FROM records WHERE user_id = ? ", (user_id,))
        return result.fetchall()[0]

    # Добавить задачу
    def add_task(self, user_id, task):
        self.cursor.execute("INSERT INTO records (user_id, task) VALUES (?, ?)", (user_id, task))
        return self.conn.commit()

    # Удалить задачу
    def remove_task(self, user_id, task):
        self.cursor.execute("DELETE FROM records WHERE user_id = (?) AND task = (?)", (user_id, task))
        return self.conn.commit()

    # Проверка задач
    def check_list(self, user_id, within="*"):
        result = self.cursor.execute("SELECT task FROM records WHERE user_id = ?", (user_id,))
        return result.fetchall()

    def close(self):
        self.conn.close()
