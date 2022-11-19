from aiogram import types, Dispatcher
from states import Questionnaire


admins_list = []


def register_questionnaire_handlers(dp1: Dispatcher):
    dp1.register_message_handler(enable_admin_rights, commands=['admin'])


async def enable_admin_rights(message: types.Message):
    admins_list.append({"admin_id": message.from_user.id, "is_free": True})
    await message.answer('Вы стали администратором!')
    try_send_files_somebody()


def try_send_files_somebody():
    pass
