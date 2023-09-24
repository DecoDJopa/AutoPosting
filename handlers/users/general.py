from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.builtin import CommandStart
from aiogram.types import CallbackQuery

from data.config import ADMINS
from filters import IsNotSubscribed
from keyboards.inline.menu import admin_menu, main_menu, back_to_main_menu
from loader import dp
from utils.db_api.db_commands import *


# ========================INFO BUTTON========================
@dp.callback_query_handler(text="inf")
async def support(call: CallbackQuery):
    await call.message.edit_text("<b>👋 Привет, данный бот создан для удобного авто~постинга во все чаты телеграмма!\n\n"
                                 "♻️ Отправлять любому юзеру своё сообщение от добавленного аккаунта!\n"
                                 "♻️ Добавление 100+ чатов\n"
                                 "♻️Включать / отключать рассылки.\n"
                                 "♻️Менять все параметры, задержки / текст / фото / и другие!\n\n"
                                 "🚀Привет от Жопы и спасибо 𝐎𝐅𝐅𝐑𝐈𝐃𝐃𝐄𝐑</b>",
                                 reply_markup=back_to_main_menu)


@dp.callback_query_handler(text="back_to_main_menu", state="*")
async def support(call: CallbackQuery, state: FSMContext):
    await state.finish()
    user = await select_user(call.from_user.id)
    if not call.message.photo:
        await call.message.edit_text(text=f"👋Привет, <code>{call.from_user.first_name}</code>,"
                                          f" нажимай кнопки снизу чтобы управлять ботом!",
                                     reply_markup=main_menu(user[4], call.from_user.id))
    else:
        await call.message.delete()
        await call.message.answer(text=f"👋Привет, <code>{call.from_user.first_name}</code>,"
                                       f" нажимай кнопки снизу чтобы управлять ботом!",
                                  reply_markup=main_menu(user[4], call.from_user.id))


@dp.callback_query_handler(IsNotSubscribed())
async def answer_call(call: CallbackQuery):
    await call.message.answer("❗️У вас нет активной подписки, для покупки доступа к боту пишите @liprikon65877\n\n"
                              "💰Цена подписки - 300₽/месяц")
    await set_not_active(call.from_user.id)


# ========================DELETE BROADCAST MESSAGE========================
# WITH STATE
@dp.callback_query_handler(text="delete_this_message", state="*")
async def del_broadcast_msg(call: CallbackQuery):
    await call.message.delete()


# ========================SHOW MAIN MENU========================
# /start WITHOUT STATE
@dp.message_handler(CommandStart())
async def bot_start(message: types.Message):
    if not await select_user(message.from_user.id):
        await add_user(message.from_user.id)

    user = await select_user(message.from_user.id)
    await message.answer(text=f"👋Привет, <code>{message.from_user.first_name}</code>,"
                              f" нажимай кнопки снизу чтобы управлять ботом!",
                         reply_markup=main_menu(user[4], message.from_user.id))



# BACK FROM ANY HANDLER TO MAIN MENU WITH STATE
@dp.callback_query_handler(text="back_admin", state="*")
async def support(call: CallbackQuery, state: FSMContext):
    await state.finish()
    if str(call.from_user.id) in ADMINS:
        await call.message.edit_text("Админ-меню", reply_markup=admin_menu)
