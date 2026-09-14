import aiosqlite
import datetime
import random
import string

DB_NAME = "database.db"


async def init_db():
    # ПОДКЛЮЧЕНИЕ К БД
    async with aiosqlite.connect(DB_NAME) as db:

        # СОЗДАНИЕ ТАБЛИЦЫ users
        await db.execute("""CREATE TABLE IF NOT EXISTS users (
                user_id INTEGER,
                name TEXT,
                username TEXT)
                """)
        await db.commit()

        # СОЗДАНИЕ ТАБЛИЦЫ админ
        await db.execute("""CREATE TABLE IF NOT EXISTS admin (
                user_id INTEGER)
                """)

        await db.commit()

        # СОЗДАНИЕ ТАБЛИЦЫ супер админ
        await db.execute("""CREATE TABLE IF NOT EXISTS blocked_users (
               user_id INTEGER,
               data TEXT)""")

        await db.commit()

        await db.execute("""CREATE TABLE IF NOT EXISTS payments (
                       user_id INTEGER,
                       data TEXT,
                       operation_id TEXT, 
                       short_key TEXT
                       )""")
        await db.commit()

        await db.execute("""CREATE TABLE IF NOT EXISTS super_admin (
                        user_id INTEGER
                        )""")
        await db.commit()





# ФУНКЦИИ DATABASE
async def add_user(user_id, name, username):
    async with aiosqlite.connect(DB_NAME) as db:
        async with db.execute("""SELECT user_id FROM users WHERE user_id = ?""", (user_id,)) as cursor:
            user = await cursor.fetchone()
            if user is None:
                await db.execute("""INSERT INTO users (user_id, name, username) VALUES (?,?,?)""", (user_id, name, username))
                await db.commit()
                return "Ты добавлен в базу ✅"

            else:
                user = "Ты уже есть в базе ❌\nЕсть информация о тебе в БД ✅\n"
            return user

async def get_user(user_id):
    async with aiosqlite.connect(DB_NAME) as db:
        async with db.execute("""SELECT user_id, name, username FROM users WHERE user_id = ?""", (user_id,)) as cursor:
            user = await cursor.fetchone()
            return user

async def update_user(user_id, new_name):
    async with aiosqlite.connect(DB_NAME) as db:
        await db.execute("""UPDATE users SET name = ? WHERE user_id = ?""", (new_name, user_id,))
        await db.commit()

async def delete_user(user_id):
    async with aiosqlite.connect(DB_NAME) as db:
        await db.execute("""DELETE FROM users WHERE user_id = ?""", (user_id, ))
        await db.commit()

async def delete_all_users():
    async with aiosqlite.connect(DB_NAME) as db:
        await db.execute("""DELETE FROM users""")
        await db.commit()

async def search_user(user_id):
    async with aiosqlite.connect(DB_NAME) as db:
        async with db.execute("""SELECT * FROM users WHERE user_id = ?""", (user_id,)) as cursor:
            return await cursor.fetchall()

async def all_users():
    async with aiosqlite.connect(DB_NAME) as db:
        async with db.execute("""SELECT * FROM users""") as cursor:
            return await cursor.fetchall()

# админ
async def add_admin(user_id):
    async with aiosqlite.connect(DB_NAME) as db:
        await db.execute("""INSERT INTO admin (user_id) VALUES (?)""", (user_id,))
        await db.commit()

async def delete_admin(user_id):
    async with aiosqlite.connect(DB_NAME) as db:
        await db.execute("""DELETE FROM admin WHERE user_id = ?""", (user_id, ))
        await db.commit()

async def search_admin(user_id):
    async with aiosqlite.connect(DB_NAME) as db:
        async with db.execute("""SELECT * FROM admin WHERE user_id = ?""", (user_id,)) as cursor:
            return await cursor.fetchall()

async def all_admins():
    async with aiosqlite.connect(DB_NAME) as db:
        async with db.execute("""SELECT * FROM admin""") as cursor:
            return await cursor.fetchall()

#СУПЕР АДМИН

async def search_super_admin(user_id):
    async with aiosqlite.connect(DB_NAME) as db:
        async with db.execute("""SELECT * FROM super_admin WHERE user_id = ?""", (user_id,)) as cursor:
           return await cursor.fetchone()

#ЗАБЛОКИРОВАННЫЕ ПОЛЬЗОВАТЕЛИ


async def add_blocked_user(user_id):
    data = datetime.datetime.now().strftime("%d.%m.%Y %H:%M:%S")
    async with aiosqlite.connect(DB_NAME) as db:
        await db.execute("""INSERT INTO blocked_users (user_id, data) VALUES (?, ?)""", (user_id, data))
        await db.commit()


async def all_blocked_users():
    async with aiosqlite.connect(DB_NAME) as db:
        async with db.execute("""SELECT * FROM blocked_users""") as cursor:
            return await cursor.fetchall()

async def search_blocked_user(user_id):
    async with aiosqlite.connect(DB_NAME) as db:
        async with db.execute("SELECT * FROM blocked_users WHERE user_id = ?", (user_id,)) as cursor:
            return await cursor.fetchall()

async def delete_blocked_user(user_id):
    async with aiosqlite.connect(DB_NAME) as db:
        await db.execute("DELETE FROM blocked_users WHERE user_id = ?", (user_id, ))
        await db.commit()

async def unblock_blocked_user(user_id):
    async with aiosqlite.connect(DB_NAME) as db:
        await db.execute("DELETE FROM blocked_users WHERE user_id = ?", (user_id,))
        await db.commit()

async def add_SUPER_admin(user_id):
    async with aiosqlite.connect(DB_NAME) as db:
        await db.execute("INSERT INTO super_admin (user_id) VALUES (?)", (user_id,))
        await db.commit()
# ИСТОРИЯ ОПЛАТ


async def add_payment(user_id, operation_id):
    data = datetime.datetime.now().strftime("%d.%m.%Y %H:%M:%S")
    text = string.ascii_letters + "1234567890"
    short_key = "#" + "".join(random.choices(text, k=5))
    async with aiosqlite.connect(DB_NAME) as db:
        await db.execute("""INSERT INTO payments (user_id, operation_id, data, short_key) VALUES (?, ?, ?, ?)""", (user_id, operation_id, data, short_key))
        await db.commit()
        return short_key

async def get_operation_id(operation_id):
    async with aiosqlite.connect(DB_NAME) as db:
        async with db.execute("""SELECT operation_id FROM payments WHERE short_key = ?""", (operation_id, )) as cursor:
            result = await cursor.fetchone()
    return result[0]

async def get_short_key(operation_id):
    async with aiosqlite.connect(DB_NAME) as db:
        async with db.execute("""SELECT short_key FROM payments WHERE operation_id = ?""", (operation_id, )) as cursor:
            result = await cursor.fetchone()
            if result:
                return result[0]

async def get_history_payments(user_id):
    async with aiosqlite.connect(DB_NAME) as db:
        async with db.execute("""SELECT user_id, operation_id, data, short_key FROM payments WHERE user_id = ?""", (user_id,)) as cursor:
            return await cursor.fetchall()