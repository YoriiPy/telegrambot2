from aiogram.utils.keyboard import InlineKeyboardBuilder


async def get_admin_start_keyboard():
    admin_start_keyboard = InlineKeyboardBuilder()
    admin_start_keyboard = InlineKeyboardBuilder()
    admin_start_keyboard.button(text="👤 Профиль", callback_data="profile", style="success")
    admin_start_keyboard.button(text='📝 Пользователи', callback_data="users", style="success")
    admin_start_keyboard.button(text="👮 Админ", callback_data="admin", style="primary")
    admin_start_keyboard.adjust(2, 1)

    return admin_start_keyboard.as_markup()

async def get_user_start_keyboard():
    user_start_keyboard = InlineKeyboardBuilder()
    user_start_keyboard.button(text="👤 Профиль", callback_data="profile", style="success")
    user_start_keyboard.button(text='📝 Пользователи', callback_data="users", style="success")
    user_start_keyboard.button(text="💵 Платежи", callback_data="history_payments", style="success")
    user_start_keyboard.button(text="‍💻 Поддержка", callback_data="support", style="primary")
    user_start_keyboard.button(text="👮 Купить админа", callback_data="buy_admin", style="primary")

    user_start_keyboard.adjust(1, 1)

    return user_start_keyboard.as_markup()



yes_or_no_keyboard = InlineKeyboardBuilder()
yes_or_no_keyboard.button(text="Да ✅", callback_data="yes_delete_db", style="primary")
yes_or_no_keyboard.button(text="Нет ❌", callback_data="no_delete_db", style="danger")
yes_or_no_keyboard.button(text="Назад ⬅️", callback_data="back_to_super_admin_menu")
yes_or_no_keyboard.adjust(2, 1)

async def get_super_admin_keyboard_menu():
    admin_keyboard = InlineKeyboardBuilder()
    admin_keyboard.button(text="👤 Пользователи", callback_data="super_admin_or_admin_for_users", style="success")
    admin_keyboard.button(text="👮 Админы", callback_data="super_admin_for_admins", style="primary")
    admin_keyboard.button(text="🚫 Блокировки", callback_data="super_admin_or_admin_for_blocked_users", style="danger")
    admin_keyboard.button(text="📝 БД", callback_data="delete_all_users")
    admin_keyboard.button(text="Назад ⬅️", callback_data="back_to_starts")

    admin_keyboard.adjust(1, 1, 1, 1)
    return admin_keyboard.as_markup()

async def get_admin_keyboard_menu():
    super_admin_keyboard = InlineKeyboardBuilder()
    super_admin_keyboard.button(text="👤 Пользователи", callback_data="super_admin_or_admin_for_users", style="primary")
    super_admin_keyboard.button(text="🚫 Блокировки", callback_data="super_admin_or_admin_for_blocked_users", style="danger")
    super_admin_keyboard.button(text="➡️ Назад", callback_data="back_to_start_admin")
    return super_admin_keyboard.as_markup()

async def get_return_start_keyboard():
    return_start_keyboard = InlineKeyboardBuilder()
    return_start_keyboard.button(text="Назад ⬅️", callback_data="back_to_start")
    return return_start_keyboard.as_markup()





async def get_admin_keyboard_menu():
    admin_keyboard = InlineKeyboardBuilder()
    admin_keyboard.button(text="👤 Пользователи", callback_data="super_admin_or_admin_for_users")
    admin_keyboard.button(text="🚫 Блокировки", callback_data="super_admin_or_admin_for_blocked_users")
    admin_keyboard.adjust(1, 1)
    return admin_keyboard.as_markup()

async def get_back_to_menu_admin_keyboard():
    back_to_menu_admin_keyboard = InlineKeyboardBuilder()
    back_to_menu_admin_keyboard.button(text="Назад ⬅️", callback_data="get_back_to_menu_admin_keyboard")
    return back_to_menu_admin_keyboard.as_markup()

async def get_return_admin_keyboard():
    return_admin_keyboard = InlineKeyboardBuilder()
    return_admin_keyboard.button(text="Назад ⬅️", callback_data="get_back_to_menu_admin_keyboard")
    return return_admin_keyboard.as_markup()

async def get_reply_admin_keyboard():
    reply_admin_keyboard = InlineKeyboardBuilder()
    reply_admin_keyboard.button(text="Ответить 👤", callback_data="reply_admin")
    return reply_admin_keyboard.as_markup()


async def back_to_starts():
    back_to_start_keyboard = InlineKeyboardBuilder()
    back_to_start_keyboard.button(text="Назад ⬅️", callback_data="back_to_start")
    return back_to_start_keyboard.as_markup()

async def func_admin_for_users(user_id):
    admin_keyboard = InlineKeyboardBuilder()
    admin_keyboard.button(text="🔎 Найти пользователя", callback_data="search_user_profile", style="success")
    admin_keyboard.button(text="👤 Удалить пользователя", callback_data="delete_users", style="success")
    admin_keyboard.button(text="➡️ Назад", callback_data="get_back_to_menu_admin_keyboard", style="primary")
    admin_keyboard.adjust(1, 1, 1)
    return admin_keyboard.as_markup()


async def func_admin_for_admins():
    admin_keyboard = InlineKeyboardBuilder()

    admin_keyboard.button(text="👮 Добавить Админа", callback_data="add_admin", style="primary")
    admin_keyboard.button(text="👮 Удаление админа", callback_data="delete_admin", style="primary")
    admin_keyboard.button(text="📢 Рассылка", callback_data="BroadCast_admin", style="primary")
    admin_keyboard.button(text="➡️ Назад", callback_data="get_back_to_menu_admin_keyboard", style="success")
    admin_keyboard.adjust(1, 1, 1, 1)
    return admin_keyboard.as_markup()


async def func_super_admin_for_admin_return():
    admin_keyboard = InlineKeyboardBuilder()
    admin_keyboard.button(text="➡️ Назад", callback_data="return_super_admin_for_admin", style="success")
    return admin_keyboard.as_markup()

async def block_users():
    admin_keyboard = InlineKeyboardBuilder()
    admin_keyboard.button(text="🚫 Block User", callback_data="block_user")
    admin_keyboard.button(text="🚫 UnBlock User", callback_data="unblock_user")
    admin_keyboard.button(text="➡️ Назад", callback_data="admin")
    admin_keyboard.adjust(1, 1, 1)
    return admin_keyboard.as_markup()



async def get_return_super_admin_block():
    return_super_admin_keyboard = InlineKeyboardBuilder()
    return_super_admin_keyboard.button(text="➡️ Назад", callback_data="return_block_super_admin_keyboard")
    return return_super_admin_keyboard.as_markup()

async def get_return_super_admin_admin_keyboard_block():
    admin_keyboard = InlineKeyboardBuilder()
    admin_keyboard.button(text="⬅️ Назад️", callback_data="get_back_to_menu_admin_keyboard")
    return admin_keyboard.as_markup()

