import sqlite3
import datetime
import random
import string
db = sqlite3.connect('database.db')
cursor = db.cursor()
import os


cursor.execute("""CREATE TABLE IF NOT EXISTS users (
                user_id INTEGER,
                name TEXT,
                username TEXT)""")
db.commit()




# ФУНКЦИИ DATABASE
def add_user(user_id, name, username):
    cursor.execute("""SELECT user_id FROM users WHERE user_id = ?""", (user_id,))
    user = cursor.fetchone()
    if user is None:
        cursor.execute("""INSERT INTO users (user_id, name, username) VALUES (?,?,?)""", (user_id, name, username))
        db.commit()
        return "Ты добавлен в базу ✅"

    else:
        user = "Ты уже есть в базе ❌\nЕсть информация о тебе в БД ✅\n"
    return user

def get_user(user_id):
    cursor.execute("""SELECT user_id, name, username FROM users WHERE user_id = ?""", (user_id,))
    user = cursor.fetchone()
    return user

def update_user(user_id, new_name):
    cursor.execute("""UPDATE users SET name = ? WHERE user_id = ?""", (new_name, user_id,))
    db.commit()

def delete_user(user_id):
    cursor.execute("""DELETE FROM users WHERE user_id = ?""", (user_id, ))
    db.commit()

def delete_all_users():
    cursor.execute("""DELETE FROM users""")
    db.commit()

def search_user(user_id):
    cursor.execute("""SELECT * FROM users WHERE user_id = ?""", (user_id,))
    return cursor.fetchall()

def all_users():
    cursor.execute("""SELECT * FROM users""")
    return cursor.fetchall()

# админ
cursor.execute("""CREATE TABLE IF NOT EXISTS admin (
                user_id INTEGER)""")
def add_admin(user_id):
    cursor.execute("""INSERT INTO admin (user_id) VALUES (?)""", (user_id,))
    db.commit()

def delete_admin(user_id):
    cursor.execute("""DELETE FROM admin WHERE user_id = ?""", (user_id, ))
    db.commit()

def search_admin(user_id):
    cursor.execute("""SELECT * FROM admin WHERE user_id = ?""", (user_id,))
    return cursor.fetchall()

def all_admins():
    cursor.execute("""SELECT * FROM admin""")
    return cursor.fetchall()

#СУПЕР АДМИН
cursor.execute("""CREATE TABLE IF NOT EXISTS super_admin (
                user_id INTEGER
                )""")

def search_super_admin(user_id):
    cursor.execute("""SELECT * FROM super_admin WHERE user_id = ?""", (user_id,))
    return cursor.fetchone()

#ЗАБЛОКИРОВАННЫЕ ПОЛЬЗОВАТЕЛИ
cursor.execute("""CREATE TABLE IF NOT EXISTS blocked_users (
               user_id INTEGER,
               data TEXT)""")

def add_blocked_user(user_id):
    data = datetime.datetime.now().strftime("%d.%m.%Y %H:%M:%S")
    cursor.execute("""INSERT INTO blocked_users (user_id, data) VALUES (?, ?)""", (user_id, data))
    db.commit()
def all_blocked_users():
    cursor.execute("""SELECT * FROM blocked_users""")
    return cursor.fetchall()

def search_blocked_user(user_id):
    cursor.execute("SELECT * FROM blocked_users WHERE user_id = ?", (user_id,))
    return cursor.fetchall()

# ИСТОРИЯ ОПЛАТ
cursor.execute("""CREATE TABLE IF NOT EXISTS payments (
               user_id INTEGER,
               data TEXT,
               operation_id TEXT, 
               short_key TEXT
               )""")

def add_payment(user_id, operation_id):
    data = datetime.datetime.now().strftime("%d.%m.%Y %H:%M:%S")
    text = string.ascii_letters + "1234567890"
    short_key = "#" + "".join(random.choices(text, k=5))
    cursor.execute("""INSERT INTO payments (user_id, operation_id, data, short_key) VALUES (?, ?, ?, ?)""", (user_id, operation_id, data, short_key))
    db.commit()
    return short_key

def get_operation_id(operation_id):
    cursor.execute("""SELECT operation_id FROM payments WHERE short_key = ?""", (operation_id, ))
    result = cursor.fetchone()
    return result[0]

def get_short_key(operation_id):
    cursor.execute("""SELECT short_key FROM payments WHERE operation_id = ?""", (operation_id, ))
    result = cursor.fetchone()
    if result:
        return result[0]

def get_history_payments(user_id):
    cursor.execute("""SELECT * FROM payments WHERE user_id = ?""", (user_id,))
    return cursor.fetchall()