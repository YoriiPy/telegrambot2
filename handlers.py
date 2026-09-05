import asyncio
from encodings import rot_13
import pay
from aiogram import Router, F, Bot
from aiogram.exceptions import TelegramBadRequest, TelegramAPIError
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery, InlineKeyboardMarkup, LabeledPrice
from aiogram.filters import Command, CommandObject
from aiogram.utils.keyboard import InlineKeyboardBuilder
from DataBase import add_user, cursor, get_user, update_user, delete_user, delete_all_users, search_user, add_admin, \
    delete_admin, search_admin, all_users, all_admins, search_super_admin, add_blocked_user, all_blocked_users, \
    add_payment, get_operation_id, get_short_key, get_history_payments, search_blocked_user
from classess import wait
from keyboards import yes_or_no_keyboard, get_admin_keyboard, get_return_start_keyboard, get_admin_start_keyboard, \
    get_user_start_keyboard, super_admin_keyboard, get_return_admin_keyboard, get_reply_admin_keyboard
from aiogram.types import PreCheckoutQuery
router = Router()

#ОБРАБОТЧИКИ КОМАНД
@router.message(Command("start"))
async def start_command(message: Message):
    user_id = message.from_user.id
    result = search_blocked_user(user_id)
    if result:
        await message.answer("Вы заблокированы ❌")
        return
    user_id = message.from_user.id
    if search_super_admin(user_id):
        if search_user(user_id):
            await message.answer(f"Ты уже есть в базе ❌\nЕсть информация о тебе в БД ✅\n\nВы СУПЕР АДМИН ✅", reply_markup = await get_admin_start_keyboard())
            delete_user(user_id)
        else:
            await message.answer(f"Ты уже есть в базе ❌\nЕсть информация о тебе в БД ✅\n\nВы СУПЕР АДМИН ✅", reply_markup=await get_admin_start_keyboard())
    elif search_admin(user_id):
        if search_user(user_id):
            await message.answer(f"Ты уже есть в базе ❌\nЕсть информация о тебе в БД ✅\n\nВы админ ✅", reply_markup = await get_admin_start_keyboard())
            delete_user(user_id)
        else:
            await message.answer(f"Ты уже есть в базе ❌\nЕсть информация о тебе в БД ✅\n\nВы админ ✅", reply_markup = await get_admin_start_keyboard())
    elif search_user(user_id):
        await message.answer(f"Ты уже есть в базе ❌\nЕсть информация о тебе в БД ✅", reply_markup= await get_user_start_keyboard())

    else:
        result = add_user(message.from_user.id, message.from_user.full_name, message.from_user.username)
        print(search_super_admin(user_id))
        await message.answer(result, reply_markup= await get_user_start_keyboard())



@router.callback_query(F.data == "users")
async def users(callback: CallbackQuery):
    user_id = callback.from_user.id
    result = search_blocked_user(user_id)
    if result:
        await callback.message.edit_text("Вы заблокированы ❌")
        return
    cursor.execute("SELECT * FROM users")
    user = cursor.fetchall()
    back_to_starts = InlineKeyboardBuilder()
    back_to_starts.button(text="Назад ⬅️", callback_data="back_to_start")
    string = ""
    for users in user:
        string += f"Имя | Фамилия: {users[1]}\n"
        string += f"Username: @{users[2]}\n"
        string += f"ID: <code>{users[0]}</code>\n\n"
    cursor.execute("SELECT * FROM admin")
    string_admin = "\n"
    admins = cursor.fetchall()
    for admin in admins:
        string_admin += str(f"{admin[0]}\n")
    if string:
        await callback.message.edit_text(f"Пользователи:\n{string}Админы: {string_admin}", parse_mode="HTML", reply_markup=back_to_starts.as_markup())
    else:
        await callback.message.edit_text(f"Пользователи:\n{string}нету\n\nАдмины: {string_admin}", parse_mode="HTML", reply_markup=back_to_starts.as_markup())


#ОБРАБОТЧИКИ CALLBACK
@router.callback_query(F.data == "profile")
async def profile_callback(callback: CallbackQuery):
    user_id = callback.from_user.id
    result = search_blocked_user(user_id)
    if result:
        await callback.message.edit_text("Вы заблокированы ❌")
        return
    await callback.answer()
    user_id = callback.from_user.id
    name = callback.from_user.full_name
    username = callback.from_user.username
    back_to_start_keyboard = InlineKeyboardBuilder()
    back_to_start_keyboard.button(text="Изменить имя 📝", callback_data="edit_to_name")
    back_to_start_keyboard.button(text="Назад ⬅️", callback_data="back_to_start")
    back_to_start_keyboard.adjust(1, 1)
    add_user(user_id, name, username)
    user = get_user(callback.from_user.id)
    user_search_admin = search_admin(user_id)
    user_search_user = search_user(user_id)
    user_search_super_admin = search_super_admin(user_id)
    if user_search_user:
        await callback.message.edit_text(
            f"👤 Профиль\n\n"
            f"Имя: {user[1]}\n"
            f"Username: {user[2]}\n"
            f"ID: <code>{user[0]}</code>\n",
            parse_mode="HTML",
            reply_markup=back_to_start_keyboard.as_markup())

    elif search_admin(user_id):
        await callback.message.edit_text(
            f"👤 Профиль\n\n"
            f"Имя: {user[1]}\n"
            f"Username: {user[2]}\n"
            f"ID: <code>{user[0]}</code>\n",
            parse_mode="HTML",
            reply_markup=back_to_start_keyboard.as_markup())
        delete_user(user_id)
    elif search_super_admin(user_id):
        await callback.message.edit_text(
            f"👤 Профиль\n\n"
            f"Имя: {user[1]}\n"
            f"Username: {user[2]}\n"
            f"ID: <code>{user[0]}</code>\n",
            parse_mode="HTML",
            reply_markup=back_to_start_keyboard.as_markup())
        delete_user(user_id)





@router.callback_query(F.data == "back_to_start")
async def back_to_start(callback: CallbackQuery):
    user_id = callback.from_user.id
    result = search_blocked_user(user_id)
    if result:
        await callback.message.edit_text("Вы заблокированы ❌")
        return
    await callback.answer()
    user_id = callback.from_user.id
    user = search_admin(user_id)
    admin = search_admin(user_id)
    super_admin = search_super_admin(user_id)

    try:
        if super_admin or admin:
            await callback.message.edit_text("Ты уже есть в базе ❌\nЕсть информация о тебе в БД ✅", reply_markup= await get_admin_start_keyboard())
        elif user:
            await callback.message.edit_text("Ты уже есть в базе ❌\nЕсть информация о тебе в БД ✅", reply_markup= await get_user_start_keyboard())
    except TelegramBadRequest as e:
        if "message can't be edited" in e.message:
            await callback.message.delete()
            if user:
                await callback.message.answer("Ты уже есть в базе ❌\nЕсть информация о тебе в БД ✅", reply_markup=await get_admin_start_keyboard())
            else:
                await callback.message.answer("Ты уже есть в базе ❌\nЕсть информация о тебе в БД ✅",  reply_markup=await get_user_start_keyboard())

@router.callback_query(F.data == "edit_to_name")
async def wait_text_name(callback: CallbackQuery, state: FSMContext):
    await callback.answer()
    await callback.message.answer("Отправьте новое имя 📝")
    await state.set_state(wait.text)

@router.callback_query(F.data == "delete_users")
async def send_id_admin(callback: CallbackQuery, state: FSMContext):
    user_id = callback.from_user.id
    result = search_blocked_user(user_id)
    if result:
        await callback.message.edit_text("Вы заблокированы ❌")
        return
    await callback.answer()
    user_id = callback.from_user.id
    user = search_admin(user_id)
    await callback.answer()
    if user:
        await state.set_state(wait.text_2)
        await state.update_data(text_id=await callback.message.edit_text("Отправьте ID пользователя 👤\nКоторого желаете удалить ✅", reply_markup = await get_return_admin_keyboard()))
    else:
        await callback.message.edit_text("Вы уже исключены из админов ❌")

@router.callback_query(F.data == "delete_all_users")
async def delete_full_users(callback: CallbackQuery, state: FSMContext):
    user_id = callback.from_user.id
    result = search_blocked_user(user_id)
    if result:
        await callback.message.edit_text("Вы заблокированы ❌")
        return
    await callback.answer()
    user_id = callback.from_user.id
    if user_id == 8461039529:
        await callback.message.edit_text("Вы точно уверены ✅", reply_markup = yes_or_no_keyboard.as_markup())
        await state.set_state(wait.delete_users)
    else:
        await callback.message.edit_text("Очищать БД может только владелец бота (Гасан)")

@router.callback_query(F.data == "search_user_profile")
async def admin_search_profile_user(callback: CallbackQuery, state: FSMContext):
    user_id = callback.from_user.id
    result = search_blocked_user(user_id)
    if result:
        await callback.message.edit_text("Вы заблокированы ❌")
        return
    await callback.answer()
    user_id = callback.from_user.id
    back_to_admin_keyboard = InlineKeyboardBuilder()
    back_to_admin_keyboard.button(text="Назад ⬅️", callback_data="back_to_admin")
    if search_admin(user_id) or search_super_admin(user_id):
        send_message = await callback.message.edit_text("Отправьте ID пользователя 👤\nДля просмотра его профиля 🔎", reply_markup = await get_return_admin_keyboard())
        await state.set_state(wait.text_3)
        await state.update_data(text=send_message.message_id)

    else:
        await callback.message.edit_text("Вы уже исключены из админов ❌")

@router.callback_query(F.data == "back_to_admin")
async def back_to_admin_menu(callback: CallbackQuery, state: FSMContext):
    user_id = callback.from_user.id
    result = search_blocked_user(user_id)
    if result:
        await callback.message.edit_text("Вы заблокированы ❌")
        return
    await callback.answer()
    user_id = callback.from_user.id
    if search_super_admin(user_id):
        await callback.message.edit_text("Здравствуйте вы СУПЕР АДМИН ✅\nВ этой админке есть функции удаления", reply_markup=await super_admin_keyboard())
    elif search_admin(user_id):
        await callback.message.edit_text("Здравствуйте вы один из избранных админов ✅\nВ этой админке есть функции удаления", reply_markup=await get_admin_keyboard())
    else:
        await callback.message.edit_text("Вы не админ ❌")

@router.callback_query(F.data == "statistics")
async def statistics(callback: CallbackQuery, state: FSMContext):
    user_id = callback.from_user.id
    result = search_blocked_user(user_id)
    if result:
        await callback.message.edit_text("Вы заблокированы ❌")
        return
    await callback.answer()
    users = len(all_users())
    admins = len(all_admins())
    await callback.message.edit_text(
        f"👤 Всего пользователей:  {users}\n"
        f"👮 Всего админов:  {admins}\n"
        f"📊 Всего пользователей и админов:  {users + admins}",
        reply_markup = await get_return_admin_keyboard()
    )

@router.callback_query(F.data == "yes_delete_db")
async def accept_delete_users(callback: CallbackQuery, state: FSMContext):
    user_id = callback.from_user.id
    result = search_blocked_user(user_id)
    if result:
        await callback.message.edit_text("Вы заблокированы ❌")
        return
    await callback.answer()
    number = 6
    number_two = 0
    delete_all_users()
    while number != 0:
        await callback.message.edit_text(f"Пользователи успешно удалены ✅\nВозвращение в админку через {number}")
        number -= 1
        await asyncio.sleep(1)

@router.callback_query(F.data == "no_delete_db")
async def no_accept_delete_users(callback: CallbackQuery, state: FSMContext):
    user_id = callback.from_user.id
    result = search_blocked_user(user_id)
    if result:
        await callback.message.edit_text("Вы заблокированы ❌")
        return
    await callback.answer()
    number = 3
    send = await callback.message.answer(f"Вы неуверены ❌\nВозвращение в админку через {number}")
    await asyncio.sleep(1)
    number = 2
    while number != 0:
        await send.edit_text(f"Вы неуверены ❌\nВозвращение в админку через {number}")
        number -= 1
        await asyncio.sleep(1)
        if number == 0:
            await send.edit_text(
                "Здравствуйте вы один из избранных админов ✅\nВ этой админке есть функции удаления",
                reply_markup=await get_admin_keyboard())

@router.callback_query(F.data == "admin")
async def admin_command(callback: CallbackQuery):
    user_id = callback.from_user.id
    result = search_blocked_user(user_id)
    if result:
        await callback.message.edit_text("Вы заблокированы ❌")
        return
    user_exists = search_admin(user_id)
    user_exists_super_admin = search_super_admin(user_id)
    if user_exists_super_admin:
        await callback.message.edit_text("Здравствуйте вы СУПЕР АДМИН ✅\nВ этой админке есть функции удаления", reply_markup= await super_admin_keyboard())
    elif user_exists:
        await callback.message.edit_text("Здравствуйте вы один из избранных админов ✅\nВ этой админке есть функции удаления", reply_markup = await get_return_start_keyboard())
    elif user_exists is False:
        await callback.message.edit_text("Вы не админ ❌", reply_markup = await get_return_start_keyboard())


@router.callback_query(F.data == "delete_admin")
async def delete_admin_command(callback: CallbackQuery, state: FSMContext):
    user_id = callback.from_user.id
    result = search_blocked_user(user_id)
    if result:
        await callback.message.edit_text("Вы заблокированы ❌")
        return
    if search_super_admin(user_id):
        await callback.message.edit_text("Отправьте ID того админа которого хотите удалить 👤", reply_markup= await get_return_admin_keyboard())
        await state.set_state(wait.delete_admin)
    elif search_admin(user_id):
        await callback.message.edit_text("Отправьте ID того админа которого хотите удалить 👤", reply_markup = await get_return_admin_keyboard())
    else:
        await callback.message.edit_text("Вы не админ ❌")


@router.callback_query(F.data == "add_admin")
async def add_admin_func(callback: CallbackQuery, state: FSMContext):
    user_id = callback.from_user.id
    result = search_blocked_user(user_id)
    if result:
        await callback.message.edit_text("Вы заблокированы ❌")
        return
    if search_super_admin(user_id):
        await callback.message.edit_text("Отправьте ID чтобы добавить юзера в админы 👤", reply_markup = await get_return_admin_keyboard())
        await state.set_state(wait.new_admin)
    else:
        await callback.message.edit_text(f"Вы не СУПЕР АДМИН 👮", reply_markup = await get_return_admin_keyboard())

@router.callback_query(F.data == "BroadCast")
async def broadcast_command(callback: CallbackQuery, state: FSMContext):
    await state.update_data(messages = await callback.message.edit_text("Отправьте сообщение для рассылки 📢", reply_markup=await get_return_admin_keyboard()))
    await state.set_state(wait.broadcast_text)

@router.callback_query(F.data == "BroadCast_admin")
async def broadcast_admin_command(callback: CallbackQuery, state: FSMContext):
    user_id = callback.from_user.id
    result = search_blocked_user(user_id)
    if result:
        await callback.message.edit_text("Вы заблокированы ❌")
        return
    await callback.message.edit_text("Отправьте сообщение которое хотите отправить админам 👤✅", reply_markup= await get_return_admin_keyboard())
    await state.update_data(messages=callback.message.message_id)
    await state.set_state(wait.broadcast_text_admin)



@router.callback_query(F.data == "support")
async def support_command(callback: CallbackQuery, state: FSMContext):
    user_id = callback.from_user.id
    result = search_blocked_user(user_id)
    if result:
        await callback.message.edit_text("Вы заблокированы ❌")
        return
    await state.update_data(messages = await callback.message.edit_text("Отправьте сообщение которое хотите отправить админу 👮", reply_markup = await get_return_start_keyboard()))
    await state.update_data(user_id = callback.from_user.id)
    await state.set_state(wait.message_user_on_support)


@router.callback_query(F.data == "reply_admin")
async def reply_admin(callback: CallbackQuery, state: FSMContext):
    user_id = callback.from_user.id
    result = search_blocked_user(user_id)
    if result:
        await callback.message.edit_text("Вы заблокированы ❌")
        return
    await callback.message.edit_text("Отправьте ответ 👤")
    await state.set_state(wait.reply_message_admin)

@router.callback_query(F.data == "block_user")
async def block_user(callback: CallbackQuery, state: FSMContext):
    user_id = callback.from_user.id
    result = search_blocked_user(user_id)
    if result:
        await callback.message.edit_text("Вы заблокированы ❌")
        return
    users = all_blocked_users()
    str_users = ""
    for user in users:
        str_users += f"👤 ID: {user[0]}\n📅 Дата: {user[1]}\n\n"
    await callback.message.edit_text(f"Отправьте ID для блокировки пользователя 👤\nСписок заблокированных пользователей:\n\n{str_users}")
    await state.set_state(wait.message_block_user)

@router.callback_query(F.data == "buy_admin")
async def buy_admin_command(callback: CallbackQuery, bot: Bot):
    user_id = callback.from_user.id
    result = search_blocked_user(user_id)
    if result:
        await callback.message.edit_text("Вы заблокированы ❌")
        return
    await callback.message.delete()
    keyboard = InlineKeyboardBuilder()
    keyboard.button(text="Назад ⬅️", callback_data="back_to_start")
    keyboard.as_markup()
    payment_keyboard = InlineKeyboardBuilder()
    payment_keyboard.button(text="Оплатить 50 ⭐", pay=True)
    payment_keyboard.attach(keyboard)
    await bot.send_invoice(
        chat_id=user_id,
        title="Admin",
        description="Оплата товара 50 звездами (админка)",
        payload=f"buy_admin_{user_id}",
        provider_token="",
        currency="XTR",
        prices=[
            LabeledPrice(
                label="50 звезд",
                amount=1
            )
        ],
        reply_markup= payment_keyboard.as_markup()
    )

# ОБРАБОТЧИКИ ОЖИДАНИЙ
@router.message(wait.text)
async def update_name(message: Message, state: FSMContext):
    user_id = message.from_user.id
    result = search_blocked_user(user_id)
    if result:
        await message.edit_text("Вы заблокированы ❌")
        return
    name = message.text
    update_user(message.from_user.id, name)
    await state.clear()
    await message.answer("Успешно сохранено ✅")

@router.message(wait.text_2)
async def delete_users(message: Message, state: FSMContext):
    user_id = message.from_user.id
    result = search_blocked_user(user_id)
    if result:
        await message.edit_text("Вы заблокированы ❌")
        return
    back_to_admin_keyboard = InlineKeyboardBuilder()
    back_to_admin_keyboard.button(text="Назад ⬅️", callback_data="back_to_admin")
    user_id = message.text
    search_user(user_id)
    user = cursor.fetchall()
    text = await state.get_data()
    text_id = text["text_id"]
    if user:
        await asyncio.sleep(2)
        await message.delete()
        await text_id.delete()
        delete_user(user_id)
        await message.answer("Пользователь успешно удален ✅", reply_markup=back_to_admin_keyboard.as_markup())
    else:
        await asyncio.sleep(2)
        await message.delete()
        await text_id.delete()
        await message.answer("Такого пользователя не существует ❌", reply_markup=back_to_admin_keyboard.as_markup())
    await state.clear()

@router.message(wait.text_3)
async def send_admin_user(message: Message, bot: Bot, state: FSMContext):
    user_id = message.from_user.id
    result = search_blocked_user(user_id)
    if result:
        await message.edit_text("Вы заблокированы ❌")
        return
    string = ""
    user_id = message.text
    search_user(user_id)
    answers = cursor.fetchone()
    back_to_admin_keyboard = InlineKeyboardBuilder()
    back_to_admin_keyboard.button(text="Назад ⬅️", callback_data="back_to_admin")
    state_data = await state.get_data()
    message_bots = state_data.get("text")
    print(message_bots)
    await message.delete()
    await bot.delete_message(message.chat.id, message_bots)
    if answers:
        user = answers
        string += f"Имя | Фамилия: {user[0]}\n"
        string += f"Username: @{user[2]}\n"
        await message.answer(string, reply_markup=back_to_admin_keyboard.as_markup())
    else:
        await message.answer("Такого пользователя не существует ❌", reply_markup=back_to_admin_keyboard.as_markup())

@router.message(wait.new_admin)
async def add_admins(message: Message, state: FSMContext):
    user_id = message.from_user.id
    result = search_blocked_user(user_id)
    if result:
        await message.edit_text("Вы заблокированы ❌")
        return
    user_id = message.text
    add_admin(user_id)
    await message.answer(f"Админ '{user_id}' успешно добавлен ✅")
    await state.clear()

@router.message(wait.delete_admin)
async def delete_admins(message: Message, state: FSMContext):
    user_id = message.from_user.id
    result = search_blocked_user(user_id)
    if result:
        await message.edit_text("Вы заблокированы ❌")
        return
    user_id = message.text
    cursor.execute("""SELECT * FROM admin WHERE user_id = ?""", (user_id,))
    answers = cursor.fetchall()
    if answers:
        delete_admin(user_id)
        await message.answer("Админ успешно удален из БД ✅")
    else:
        await message.answer("Такого админа не существует ❌")
    await state.clear()

@router.message(wait.broadcast_text)
async def broadcast_wait(message: Message, state: FSMContext, bot: Bot):
    user_id = message.from_user.id
    result = search_blocked_user(user_id)
    if result:
        await message.edit_text("Вы заблокированы ❌")
        return
    counter_users = len(all_users())
    messages = message.text
    people = all_users()
    data = await state.get_data()
    send_text = data.get("messages")

    for user_id in people:
        if search_user(user_id[0]):
            await send_text.edit_text(f"Идет рассылка 📢\nОсталось {counter_users} пользователей", reply_markup=await get_return_admin_keyboard())
            await message.copy_to(chat_id=user_id[0])
            counter_users -= 1
            await asyncio.sleep(1)
            if counter_users == 0:
                await send_text.edit_text(f"Идет рассылка 📢\nОсталось 0 пользователей", reply_markup=await get_return_admin_keyboard())


@router.message(wait.message_user_on_support)
async def send_user_message_on_admin(message: Message, state: FSMContext, bot: Bot):
    user_id = message.from_user.id
    result = search_blocked_user(user_id)
    if result:
        await message.edit_text("Вы заблокированы ❌")
        return
    admin_id = search_super_admin(8461039529)[0]
    data = await state.get_data()
    user_id = data.get("user_id")
    text = f"👤 {user_id} отправляет:\n{message.text}"
    await bot.send_message(chat_id=admin_id, text=text, reply_markup = await get_reply_admin_keyboard())
    await bot.send_message(chat_id = user_id, text="Отправлено ✅")


@router.message(wait.reply_message_admin)
async def reply_messages_admin(message: Message, state: FSMContext, bot: Bot):
    user_id = message.from_user.id
    result = search_blocked_user(user_id)
    if result:
        await message.edit_text("Вы заблокированы ❌")
        return
    data = await state.get_data()
    user_id = data.get("user_id")
    text = f"👮Админ ответил:\n{message.text}"
    await bot.send_message(chat_id=user_id, text=text, reply_markup = await get_reply_admin_keyboard())

@router.message(wait.message_block_user)
async def message_block_user(message: Message, state: FSMContext, bot: Bot):
    user_id = message.from_user.id
    result = search_blocked_user(user_id)
    if result:
        await message.edit_text("Вы заблокированы ❌")
        return
    user_id = message.text
    if search_user(user_id):
        add_blocked_user(user_id)
        await message.answer("Пользователь заблокирован ✅")
    else:
        await message.answer("Такого пользователя не существует ❌")
    await state.clear()

@router.message(wait.broadcast_text_admin)
async def broadcast_to_admin(message: Message, state: FSMContext, bot: Bot):
    data = await state.get_data()
    full_text = data.get("messages")

    if full_text:
        try:
            await bot.delete_message(chat_id=message.chat.id, message_id=full_text)
        except TelegramBadRequest:
            pass

    admins = all_admins()
    len_admins = len(admins)

    status_msg = await message.answer(f"Осталось {len_admins} админов 📢")

    for admin in admins:
        try:
            await message.copy_to(chat_id=admin[0])
            len_admins -= 1
            await status_msg.edit_text(f"Идет рассылка 👮📢\nОсталось {len_admins} admin")
            await asyncio.sleep(1)
        except TelegramAPIError:
            len_admins -= 1
            try:
                await status_msg.edit_text(f"Осталось {len_admins} админов")
            except TelegramBadRequest:
                pass
            continue
        except Exception:
            len_admins -= 1
            continue

    try:
        await status_msg.edit_text("Рассылка успешно завершена! 👤✅")
    except TelegramBadRequest:
        pass

    try:
        await message.delete()
    except TelegramBadRequest:
        pass

    await state.clear()


#ОПЛАТА
@router.pre_checkout_query()
async def process_pre_checkout_query(pre_checkout_query: PreCheckoutQuery, bot: Bot):
    await bot.answer_pre_checkout_query(pre_checkout_query.id, ok=True)


@router.message(F.successful_payment)
async def success_payment_handler(message: Message, bot: Bot):
    payment = message.successful_payment
    stars_count = payment.total_amount
    payload = payment.invoice_payload
    charge_id = payment.telegram_payment_charge_id
    if payload.startswith("buy_admin"):
        user_id = message.from_user.id
        user_id = payload.split("_")[2]  # Вытаскиваем ID пользователя из payload
        add_admin(user_id)
        short_key = add_payment(user_id, charge_id)

        # 1. Пытаемся бесшумно удалить старую карточку инвойса (счета)
        try:
            # message.message_id - 1 обычно указывает на сообщение с инвойсом, отправленное перед чеком
            await bot.delete_message(chat_id=message.chat.id, message_id=message.message_id - 1)
        except Exception:
            pass  # Если инвойс уже удален или недоступен, просто игнорируем, чтобы бот не упал
        short_key = get_short_key(charge_id)
        # 2. Отправляем новое чистое сообщение с подтверждением (системный чек об оплате НЕ трогаем
        await message.answer(f"Успешно оплачено {stars_count} звезд ✅\nВы добавлены в админы 👮\nВаш сокращенный код {short_key}")

@router.message(Command("return_stars"))
async def return_stars_handler(message: Message, state: FSMContext, bot: Bot):
    await message.answer("Отправьте номер заказа ✅")
    await state.set_state(wait.number_payment)

@router.message(wait.number_payment)
async def number_payment_handler(message: Message, state: FSMContext, bot: Bot):
    user_id = message.from_user.id
    short_key = message.text
    result = get_operation_id(short_key)
    if result:
        try:
            await bot.refund_star_payment(user_id=user_id, telegram_payment_charge_id=result)
        except TelegramBadRequest as e:
            if "CHARGE_ALREADY_REFUNDED" in e.message:
                await message.answer("Платеж уже был возвращен раннее ⚠️")

    else:
        await message.answer("Такого заказа не существует ❌")

@router.callback_query(F.data == "history_payments")
async def history_payments_handler(callback: CallbackQuery, state: FSMContext, bot: Bot):
    user_id = callback.from_user.id
    result = search_blocked_user(user_id)
    if result:
        await callback.message.edit_text("Вы заблокированы ❌")
        return
    history_payments = get_history_payments(user_id)
    text = ""
    for payment in history_payments:
        text += f"{payment[0]}\n"
    if history_payments:
        await callback.message.edit_text(text)
    else:
        await callback.message.edit_text("У вас нету ни одного платежа ❌💵")


