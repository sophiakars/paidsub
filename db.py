import sqlite3
import time


class Database:
    def __init__(self, db_file):
        # обращение к БД
        self.connection = sqlite3.connect(db_file)
        # создание запросов
        self.cursor = self.connection.cursor()

    # запись пользователя в БД
    def add_user(self, user_id):
        with self.connection:
            return self.cursor.execute("INSERT INTO `users` (`user_id`) VALUES (?)", (user_id,))

    # проверка существования пользователя в БД
    def user_exists(self, user_id):
        with self.connection:
            result = self.cursor.execute("SELECT * FROM `users` WHERE `user_id` = ?", (user_id,)).fetchall()
            return bool(len(result))

    # заполение поля name
    def set_name(self, user_id, name):
        with self.connection:
            return self.cursor.execute("UPDATE `users` SET `name` = ? WHERE `user_id` = ?", (name, user_id,))

    # получение значения поля signup
    def get_signup(self, user_id):
        with self.connection:
            result = self.cursor.execute("SELECT `signup` FROM `users` WHERE `user_id` = ?", (user_id,)).fetchall()
            for row in result:
                signup = str(row[0])
            return signup

    # обновление поля signup
    def set_signup(self, user_id, signup):
        with self.connection:
            return self.cursor.execute("UPDATE `users` SET `signup` = ? WHERE `user_id` = ?", (signup, user_id,))

    # получение имени пользователя из БД
    def get_name(self, user_id):
        with self.connection:
            result = self.cursor.execute("SELECT `name` FROM `users` WHERE `user_id` = ?", (user_id,)).fetchall()
            for row in result:
                name = str(row[0])
            return name

    # запись времени подписки в БД
    def set_time_sub(self, user_id, time_sub):
        with self.connection:
            return self.cursor.execute("UPDATE `users` SET `time_sub` = ? WHERE `user_id` = ?", (time_sub, user_id,))

    # получение времени подписки из БД
    def get_time_sub(self, user_id):
        with self.connection:
            result = self.cursor.execute("SELECT `time_sub` FROM `users` WHERE `user_id` = ?", (user_id,)).fetchall()
            for row in result:
                time_sub = int(row[0])
            return time_sub

    # проверка наличия подписки
    def get_sub_status(self, user_id):
        with self.connection:
            result = self.cursor.execute("SELECT `time_sub` FROM `users` WHERE `user_id` = ?", (user_id,)).fetchall()
            for row in result:
                time_sub = int(row[0])
            if time_sub > int(time.time()):
                return True
            else:
                return False
