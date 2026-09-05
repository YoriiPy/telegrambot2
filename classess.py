from aiogram.fsm.state import StatesGroup, State


class wait(StatesGroup):
    text = State()
    text_2 = State()
    text_3 = State()
    new_admin = State()
    delete_admin = State()
    delete_users = State()
    broadcast_text = State()
    broadcast_text_admin = State()
    message_user_on_support = State()
    reply_message_admin = State()
    message_block_user = State()
    number_payment = State()