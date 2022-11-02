import datetime
import logging
import random
import sqlite3
import time

def update_format_with_args(sql, parameters: dict):
    values = ", ".join([
        f"{item} = ?" for item in parameters
    ])
    sql = sql.replace("XXX", values)
    return sql, tuple(parameters.values())

def get_format_args(sql, parameters: dict):
    sql += " AND ".join([
        f"{item} = ?" for item in parameters
    ])
    return sql, tuple(parameters.values())

class BotDB:

    def __init__(self, path_to_db):
        self.conn = sqlite3.connect(path_to_db, check_same_thread=False)
        self.cursor = self.conn.cursor()

    def user_check(self, user_id):
        """Проверяем, есть ли юзер в базе"""
        result = self.cursor.execute("SELECT `id` FROM `users` WHERE `user_id` = ?", (user_id,))
        return bool(len(result.fetchall()))

    def get_user_id(self, user_id):
        """Достаем юзера в базе по его user_id"""
        result = self.cursor.execute("SELECT * FROM `users` WHERE `user_id` = ?", (user_id,))
        result = result.fetchone()
        res = {"id": result[0], "user_id": result[1], "mode": result[2], "oboi_get": result[3]}
        return res

    def add_user(self, user_id):
        """Добавляем юзера в базу"""
        self.cursor.execute("INSERT INTO `users` (`user_id`) VALUES (?)", [user_id])
        return self.conn.commit()
    
    def update_user(self, user_id, **kwargs):
        """Изменяем параметры юзера"""
        sql = f"UPDATE `users` SET XXX WHERE `user_id` = {user_id}"
        sql, parameters = update_format_with_args(sql, kwargs)
        self.cursor.execute(sql, parameters)
        return self.conn.commit()
    
    def get_users(self):
        """Достаем всех юзеров"""
        result = self.cursor.execute("SELECT * FROM `users`")
        return result.fetchall()

    def donate_check(self, donate_id):
        """Проверяем, есть ли оплата в базе"""
        result = self.cursor.execute("SELECT `id` FROM `stats` WHERE `donate_id` = ?", (str(donate_id),))
        return bool(len(result.fetchall()))
    
    def add_parametr(self, name, value):
        """Добавляем параметр в базу"""
        self.cursor.execute("INSERT INTO setting (parametr, value) VALUES (?, ?)",
                   [name, value])
        return self.conn.commit()
    
    def get_parametrs(self):
        """Достаем все параметры"""
        result = self.cursor.execute("SELECT * FROM `setting`")
        res = result.fetchall()
        result = {}
        for i in res:
            result[i[0]] = i[1]
        return result

    def update_parametrs(self, id, **kwargs):
        """Изменяем параметры юзера"""
        sql = f"UPDATE `setting` SET XXX WHERE `parametr` = '{id}'"
        sql, parameters = update_format_with_args(sql, kwargs)
        self.cursor.execute(sql, parameters)
        return self.conn.commit()

    def add_categories(self, name):
        """Добавляем категорию в базу"""
        result = self.cursor.execute("INSERT INTO category (name) VALUES (?)",
                   [name,])
        return self.conn.commit()
    
    def get_categories(self):
        """Достаем все категории"""
        result = self.cursor.execute("SELECT * FROM `category`")
        res = result.fetchall()
        result = []
        for i in res:
            result.append(i[0])
        return result

    def get_categories_name(self, namex):
        """Достаем все категории"""
        result = self.cursor.execute("SELECT `id` FROM `category` WHERE `name` = ?", (str(namex),))
        res = result.fetchone()
        return res

    def update_categories(self, id, **kwargs):
        """Изменяем параметры юзера"""
        sql = f"UPDATE `category` SET XXX WHERE `id` = {id}"
        sql, parameters = update_format_with_args(sql, kwargs)
        self.cursor.execute(sql, parameters)
        return self.conn.commit()

    def delete_categories(self, id):
        """Изменяем параметры юзера"""
        sql = f"DELETE FROM `category` WHERE `id` = {id}"
        self.cursor.execute(sql)
        return self.conn.commit()

    def get_oboi(self, **kwargs):
        """Достаем все категории"""
        sql = "SELECT * FROM oboi WHERE "
        sql, parameters = get_format_args(sql, kwargs)
        get_response = self.cursor.execute(sql, parameters)
        res = get_response.fetchall()
        result = []
        for i in res:
            result.append([i[0], i[1]])
        return result

    def add_oboi(self, photo, category):
        """Добавляем юзера в базу"""
        self.cursor.execute("INSERT INTO `oboi` (`photo`, `category`) VALUES (?, ?)", [photo, category])
        return self.conn.commit()


    def close(self):
        """Закрываем соединение с БД"""
        self.connection.close()


