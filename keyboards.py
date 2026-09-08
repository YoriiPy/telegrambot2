from aiogram.utils.keyboard import InlineKeyboardBuilder
import asyncio

async def get_admin_start_keyboard():
    admin_start_keyboard = InlineKeyboardBuilder()
    admin_start_keyboard = InlineKeyboardBuilder()
    admin_start_keyboard.button(text="Профиль 👤", callback_data="profile", style="success")
    admin_start_keyboard.button(text='Пользователи 📝👤', callback_data="users", style="primary")
    admin_start_keyboard.button(text="Админ 👮", callback_data="admin")
    admin_start_keyboard.adjust(2, 1)

    return admin_start_keyboard.as_markup()

async def get_user_start_keyboard():
    user_start_keyboard = InlineKeyboardBuilder()
    user_start_keyboard.button(text="Профиль 👤", callback_data="profile")
    user_start_keyboard.button(text='Пользователи 📝👤', callback_data="users")
    user_start_keyboard.button(text="Поддержка 🧑‍💻", callback_data="support")
    user_start_keyboard.button(text="Купить админа 👮", callback_data="buy_admin")
    user_start_keyboard.button(text="Платежи 💵", callback_data="history_payments")
    user_start_keyboard.adjust(1, 1)

    return user_start_keyboard.as_markup()



yes_or_no_keyboard = InlineKeyboardBuilder()
yes_or_no_keyboard.button(text="Да ✅", callback_data="yes_delete_db")
yes_or_no_keyboard.button(text="Нет ❌", callback_data="no_delete_db")
yes_or_no_keyboard.button(text="Назад ⬅️", callback_data="back_to_admin")
yes_or_no_keyboard.adjust(2, 1)

async def get_admin_keyboard():
    admin_keyboard = InlineKeyboardBuilder()
    admin_keyboard.button(text="Найти пользователя 🔎", callback_data="search_user_profile")
    admin_keyboard.button(text="Удалить пользователя 👤", callback_data="delete_users")
    admin_keyboard.button(text="Очистить БД 📝", callback_data="delete_all_users")
    admin_keyboard.button(text="Статистика 📊", callback_data="statistics")
    admin_keyboard.button(text="Блок пользователя 🚫", callback_data="block_user")
    admin_keyboard.button(text="Назад ⬅️", callback_data="back_to_start")
    admin_keyboard.adjust(2, 2, 1)
    return admin_keyboard.as_markup()

async def get_return_start_keyboard():
    return_start_keyboard = InlineKeyboardBuilder()
    return_start_keyboard.button(text="Назад ⬅️", callback_data="back_to_start")
    return return_start_keyboard.as_markup()

async def super_admin_keyboard():
    super_admin_keyboard = InlineKeyboardBuilder()
    super_admin_keyboard.button(text="Найти пользователя 🔎", callback_data="search_user_profile", style="success")
    super_admin_keyboard.button(text="Удалить пользователя 👤", callback_data="delete_users", style="success")
    super_admin_keyboard.button(text="Рассылка пользователям 📢", callback_data="BroadCast", style="success")
    super_admin_keyboard.button(text="Удалить админа 👮", callback_data="delete_admin", style="primary")
    super_admin_keyboard.button(text="Добавить админа 👮", callback_data="add_admin", style="primary")
    super_admin_keyboard.button(text="Рассылка админам 👮", callback_data="BroadCast_admin", style="primary")
    super_admin_keyboard.button(text="Статистика 📊", callback_data="statistics", style="primary")
    super_admin_keyboard.button(text="Блок пользователя 🚫", callback_data="block_user", style="danger")
    super_admin_keyboard.button(text="Разблок пользователя 🚫", callback_data="unblock_user", style="danger")
    super_admin_keyboard.button(text="Очистить БД 📝", callback_data="delete_all_users", style="danger")
    super_admin_keyboard.button(text="Назад ⬅️", callback_data="back_to_start")
    super_admin_keyboard.adjust(3, 3, 3, 1, 1)

    return super_admin_keyboard.as_markup()

async def get_return_admin_keyboard():
    return_admin_keyboard = InlineKeyboardBuilder()
    return_admin_keyboard.button(text="Назад ⬅️", callback_data="back_to_admin")
    return return_admin_keyboard.as_markup()

async def get_reply_admin_keyboard():
    reply_admin_keyboard = InlineKeyboardBuilder()
    reply_admin_keyboard.button(text="Ответить 👤", callback_data="reply_admin")
    return reply_admin_keyboard.as_markup()


async def back_to_starts():
    back_to_start_keyboard = InlineKeyboardBuilder()
    back_to_start_keyboard.button(text="Назад ⬅️", callback_data="back_to_start")
    return back_to_start_keyboard.as_markup()