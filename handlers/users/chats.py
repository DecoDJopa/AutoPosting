import os
import random
from datetime import datetime

from aiogram.dispatcher import FSMContext
from aiogram.types import CallbackQuery, Message
from telethon import TelegramClient

from keyboards.inline.menu import all_chats_menu, in_chat_menu, back_to_main_menu, api_hash, api_id, code_menu, \
    accounts_menu, multi_settings_menu
from loader import dp, scheduler
from states.states import EditChat, AddAccount, AddChat, SendMessageState, MultiEdit
from utils.db_api.db_commands import select_user, select_chat, del_chat, update_text, update_delay, update_pic, \
    update_session, add_chat, update_is_active, check_delay, del_all_chats, set_not_active, add_acc, \
    select_user_accounts, del_acc, del_chats_by_num, select_user_chats, update_all_pic, update_all_text, \
    del_all_chats_number, select_chat_num
# ===============CHATS===========
# SHOW ALL CHATS
from utils.other_utils import send_message_to_chat, send_message_to_user, get_valid_date, get_user_chats


@dp.callback_query_handler(text="all_accounts")
async def all_accounts(call: CallbackQuery):
    user = await select_user(call.from_user.id)
    if user[3]:
        date_when_expired = await get_valid_date(user)
        if datetime.now() < date_when_expired:
            await call.message.edit_text("<b>Выберите аккаунт или добавьте новый.</b>",
                                         reply_markup=await accounts_menu(call.from_user.id))
        else:
            await call.message.answer("❗️У вас нет активной подписки, для покупки доступа к боту пишите @liprikon65877\n\n"
                              "💰Цена подписки - 300₽/месяц")
            await set_not_active(call.from_user.id)
    else:
        await call.message.answer("❗️У вас нет активной подписки, для покупки доступа к боту пишите @liprikon65877\n\n"
                              "💰Цена подписки - 300₽/месяц")


@dp.callback_query_handler(text_startswith="accounts:")
async def accounts(call: CallbackQuery):
    number = call.data.split(":")[1]
    await call.message.edit_text("<b>Выберите или добавьте чат</b>",
                                 reply_markup=await all_chats_menu(call.from_user.id, number))


@dp.callback_query_handler(text_startswith="del_acc:")
async def delete_acc(call: CallbackQuery):
    number = call.data.split(":")[1]
    chats = await select_user_chats(call.from_user.id, number)
    for chat in chats:
        if chat[6] == 1:
            job = scheduler.get_job(job_id=f"{call.from_user.id}:{chat[8]}")
            job.remove()
    os.remove(f"sessions/{number}.session")
    await del_acc(call.from_user.id, number)
    await del_chats_by_num(call.from_user.id, number)
    await call.message.edit_text("<b>Аккаунт был удален</b>", reply_markup=await accounts_menu(call.from_user.id))


@dp.callback_query_handler(text_startswith="import_chats:")
async def delete_acc(call: CallbackQuery):
    number = call.data.split(":")[1]
    chats = await get_user_chats(number)
    for chat in chats:
        if chat.to_dict().get("entity").to_dict().get('_') == "User":
            continue
        name = chat.to_dict().get("name")
        user_id = chat.to_dict().get("name")
        if await select_chat_num(number, user_id):
            continue
        chat_id = random.randint(10000000, 99999999)
        await add_chat(call.from_user.id, name, user_id, chat_id, number)
    await call.message.edit_text("<b>Выберите или добавьте чат</b>",
                                 reply_markup=await all_chats_menu(call.from_user.id, number))


@dp.callback_query_handler(text_startswith="multi_settings:")
async def multi_settings(call: CallbackQuery):
    number = call.data.split(":")[1]
    await call.message.edit_text("<b>Выберите нужную вам функцию:</b>", reply_markup=multi_settings_menu(number))


# EDIT SOMETHING IN BROADCAST MESSAGE
@dp.callback_query_handler(text_startswith="multi`")
async def show_chat(call: CallbackQuery, state: FSMContext):
    option, number = call.data.split("`")[1], call.data.split("`")[2]
    all_chats = await select_user_chats(call.from_user.id, number)
    if option == "del":
        await del_all_chats_number(number)
        await call.message.edit_text("<b>💬Добавить или редактировать чаты можно в данном разделе:</b>",
                                     reply_markup=await all_chats_menu(call.from_user.id, number))
        for chat in all_chats:
            if chat[6] == 1:
                scheduler.remove_job(job_id=f"{call.from_user.id}:{chat[8]}")

    elif option == "turn_on":
        for chat in all_chats:
            if chat[3]:
                if chat[5]:
                    if chat[6] == 1:
                        continue
                    else:
                        chat_type = 1
                        job = scheduler.add_job(
                            send_message_to_chat,
                            "interval", minutes=chat[3],
                            args=(call.from_user.id, chat[2], chat[8]),
                            id=f"{call.from_user.id}:{chat[8]}"
                        )
                        await update_is_active(call.from_user.id, chat[8], 1)
                else:
                    continue
            else:
                continue

    elif option == "turn_off":
        for chat in all_chats:
            if chat[6] == 0:
                continue
            scheduler.remove_job(job_id=f"{call.from_user.id}:{chat[8]}")
            await update_is_active(call.from_user.id, chat[8], 0)

    else:
        if option == "text":
            text = "<b>Напишите новый текст.</b>"


        elif option == "photo":
            text = "<b>Отправьте новую ссылку на фото.\nВажно, чтобы ссылка заканчивалась на" \
                   " <code>.png</code> или <code>.jpeg</code>\n⚠️Можно сделать тут: @imgurbot_bot</b>"

        else:
            text = "<b>Извините, произошла ошибка</b>"
        msg_to_edit = await call.message.edit_text(text,
                                                   reply_markup=back_to_main_menu)

        await MultiEdit.EC1.set()
        await state.update_data(option=option, msg_to_edit=msg_to_edit, number=number)


# RECEIVE ARGUMENT TO UPDATE BROADCAST MESSAGE
@dp.message_handler(state=MultiEdit.EC1)
async def receive_new_chat_atr(message: Message, state: FSMContext):
    data = await state.get_data()
    option, msg_to_edit, argument, number = data.get("option"), data.get("msg_to_edit"), message.text, data.get(
        "number")

    await message.delete()
    if option == "text":
        await update_all_text(number, argument)

    elif option == "photo":
        await update_all_pic(number, argument)

    all_chats = await select_user_chats(message.from_user.id, number)
    for chat in all_chats:
        if chat[6] == 1:
            scheduler.remove_job(job_id=f"{message.from_user.id}:{chat[8]}")
            scheduler.add_job(
                send_message_to_chat,
                "interval", minutes=chat[3],
                args=(message.from_user.id, chat[2], chat[8]),
                id=f"{message.from_user.id}:{chat[8]}"
            )
    await msg_to_edit.edit_text("<b>Выберите или добавьте чат</b>",
                                reply_markup=await all_chats_menu(message.from_user.id, number))
    await state.finish()


# SHOW BROADCAST MESSAGE
@dp.callback_query_handler(text_startswith="uc::")
async def show_chat(call: CallbackQuery):
    chat_id = call.data.split("::")[1]
    chat = await select_chat(call.from_user.id, chat_id)
    scheduler_job = scheduler.get_job(f"{call.from_user.id}:{chat[8]}")
    next_run = "Не указано" if not scheduler_job else scheduler_job.next_run_time
    await call.message.edit_text(f"<b>🆔CHAT: <code>{chat[2]}</code>\n\n"
                                 f"💭Текст: {chat[5]}\n\n"
                                 f"🖼Картинка: {chat[4]}\n\n"
                                 f"🕰Задержка: <code>{chat[3]} мин.</code>\n"
                                 f"📮Отправка: <code>"
                                 f"{next_run}</code></b>",
                                 reply_markup=in_chat_menu(chat[6], chat_id, chat[9]), disable_web_page_preview=True)


# EDIT SOMETHING IN BROADCAST MESSAGE
@dp.callback_query_handler(text_startswith="ed`")
async def show_chat(call: CallbackQuery, state: FSMContext):
    option, chat_id = call.data.split("`")[1], call.data.split("`")[2]
    chat = await select_chat(call.from_user.id, chat_id)
    scheduler_job = scheduler.get_job(f"{call.from_user.id}:{chat[8]}")
    next_run = "Не указано" if not scheduler_job else scheduler_job.next_run_time

    if option == "del":
        await del_chat(call.from_user.id, chat_id)
        await call.message.edit_text("<b>💬Добавить или редактировать чаты можно в данном разделе:</b>",
                                     reply_markup=await all_chats_menu(call.from_user.id, chat[9]))
        scheduler.remove_job(job_id=f"{call.from_user.id}:{chat[8]}")
    elif option == "turn":
        if chat[3]:
            if chat[5]:
                if chat[6] == 1:
                    chat_type = 0
                    scheduler.remove_job(job_id=f"{call.from_user.id}:{chat[8]}")
                    await update_is_active(call.from_user.id, chat[8], 0)
                    next_run = "Не указано"
                else:
                    chat_type = 1
                    job = scheduler.add_job(
                        send_message_to_chat,
                        "interval", minutes=chat[3],
                        args=(call.from_user.id, chat[2], chat[8]),
                        id=f"{call.from_user.id}:{chat[8]}"
                    )
                    await update_is_active(call.from_user.id, chat[8], 1)
                    next_run = job.next_run_time
                await call.message.edit_text(f"<b>🆔CHAT: <code>{chat[2]}</code>\n\n"
                                             f"💭Текст: {chat[5]}\n\n"
                                             f"🖼Картинка: {chat[4]}\n\n"
                                             f"🕰Задержка: <code>{chat[3]} мин.</code>\n"
                                             f"📮Отправка: <code>"
                                             f"{next_run}</code></b>",
                                             reply_markup=in_chat_menu(chat_type, chat_id, chat[9]),
                                             disable_web_page_preview=True)
            else:
                await call.answer("❗️Текст отсутствует")
        else:
            await call.answer("❗️Задержка отсутствует")
    else:
        if option == "text":
            text = "<b>Напишите новый текст.</b>"

        elif option == "delay":
            text = "<b>Напишите новую задержку.\n\n" \
                   "♻️Вводить в минутах</b>"

        elif option == "photo":
            text = "<b>Отправьте новую ссылку на фото.\nВажно, чтобы ссылка заканчивалась на" \
                   " <code>.png</code> или <code>.jpeg</code>\n⚠️Можно сделать тут: @imgurbot_bot</b>"

        else:
            text = "<b>Извините, произошла ошибка</b>"
        msg_to_edit = await call.message.edit_text(text,
                                                   reply_markup=back_to_main_menu)

        await EditChat.EC1.set()
        await state.update_data(option=option, msg_to_edit=msg_to_edit, chat1=chat)


# RECEIVE ARGUMENT TO UPDATE BROADCAST MESSAGE
@dp.message_handler(state=EditChat.EC1)
async def receive_new_chat_atr(message: Message, state: FSMContext):
    data = await state.get_data()
    option, msg_to_edit, argument, chat = data.get("option"), data.get("msg_to_edit"), message.text, data.get("chat1")
    scheduler_job = scheduler.get_job(chat[7])
    await message.delete()
    if option == "delay":
        delay = await check_delay(message.from_user.id, int(message.text), chat[9])
        if not delay:
            await update_delay(message.from_user.id, chat[8], argument)
            chat = await select_chat(message.from_user.id, chat[8])
            await msg_to_edit.edit_text(f"<b>🆔CHAT: <code>{chat[2]}</code>\n\n"
                                        f"💭Текст: {chat[5]}\n\n"
                                        f"🖼Картинка: {chat[4]}\n\n"
                                        f"🕰Задержка: <code>{chat[3]} мин.</code>\n"
                                        f"📮Отправка: <code>{str(scheduler_job).split(' ')[-1][:-1]}</code></b>",
                                        reply_markup=in_chat_menu(chat[6], chat[8], chat[9]),
                                        disable_web_page_preview=True)
            await state.finish()
        else:
            await message.answer("<b>Канал с такой задержкой уже существует, это может привести к крашу бота,"
                                 " пожалуйста попробуйте еще раз</b>")
    else:
        if option == "text":
            await update_text(message.from_user.id, chat[8], argument)

        elif option == "photo":
            await update_pic(message.from_user.id, chat[8], argument)

        chat = await select_chat(message.from_user.id, chat[8])
        if chat[6] == 1:
            scheduler.remove_job(job_id=f"{message.from_user.id}:{chat[8]}")
            scheduler.add_job(
                send_message_to_chat,
                "interval", minutes=chat[3],
                args=(message.from_user.id, chat[2], chat[8]),
                id=f"{message.from_user.id}:{chat[8]}"
            )
        await msg_to_edit.edit_text(f"<b>🆔CHAT: <code>{chat[2]}</code>\n\n"
                                    f"💭Текст: {chat[5]}\n\n"
                                    f"🖼Картинка: {chat[4]}\n\n"
                                    f"🕰Задержка: <code>{chat[3]} мин.</code>\n"
                                    f"📮Отправка: <code>{str(scheduler_job).split(' ')[-1][:-1]}</code></b>",
                                    reply_markup=in_chat_menu(chat[6], chat[8], chat[9]), disable_web_page_preview=True)
        await state.finish()


@dp.callback_query_handler(text_startswith="add_new_chat:")
async def add_chat_first(call: CallbackQuery, state: FSMContext):
    number = call.data.split(":")[1]
    await AddChat.A1.set()
    msg_to_edit = await call.message.edit_text("<b>🚀Введите сыллку на чат:</b>", reply_markup=back_to_main_menu)
    await state.update_data(msg_to_edit=msg_to_edit, number=number)


@dp.message_handler(state=AddChat.A1)
async def receive_chat(message: Message, state: FSMContext):
    data = await state.get_data()
    msg_to_edit = data.get("msg_to_edit")
    chat_url = message.text
    await message.delete()
    await msg_to_edit.edit_text(f"<b>📜Введите текст для кнопки данного чата</b>", reply_markup=back_to_main_menu)
    await AddChat.next()
    await state.update_data(chat_url=chat_url)


@dp.message_handler(state=AddChat.A2)
async def receive_chat(message: Message, state: FSMContext):
    data = await state.get_data()
    msg_to_edit, chat_url, number = data.get("msg_to_edit"), data.get("chat_url"), data.get("number")
    name = message.text
    await message.delete()
    chat_id = random.randint(10000000, 99999999)
    await add_chat(message.from_user.id, name, chat_url, chat_id, number)
    await msg_to_edit.edit_text(f"<b>✅Чат <code>{name}</code> добавлен</b>",
                                reply_markup=await all_chats_menu(message.from_user.id, number))
    await state.finish()


# ===============SEND MESSAGE===========
@dp.callback_query_handler(text="send_message")
async def show_all_chats(call: CallbackQuery, state: FSMContext):
    user = await select_user(call.from_user.id)
    if not user[4]:
        await call.answer("❗️Сначала вам нужно добавить аккаунт в главном меню.")
    else:
        msg_to_edit = await call.message.edit_text(
            "💌<b>Введите @username человека, которому хотите отправить сообщение.</b>", reply_markup=back_to_main_menu)
        await SendMessageState.A1.set()
        await state.update_data(msg_to_edit=msg_to_edit)


@dp.message_handler(state=SendMessageState.A1)
async def get_message_text(message: Message, state: FSMContext):
    data = await state.get_data()
    msg_to_edit = data.get("msg_to_edit")
    username = message.text
    await message.delete()
    await msg_to_edit.edit_text(
        "💌<b>✉️Напишите сообщение:</b>", reply_markup=back_to_main_menu)
    await SendMessageState.next()
    await state.update_data(username=username)


@dp.message_handler(state=SendMessageState.A2)
async def get_message_text(message: Message, state: FSMContext):
    data = await state.get_data()
    msg_to_edit, username = data.get("msg_to_edit"), data.get("username")
    msg_txt = message.text
    accs = await select_user_accounts(message.from_user.id)
    number = random.choice(accs)
    await message.delete()
    await send_message_to_user(username, msg_txt, number[1])
    await msg_to_edit.edit_text(
        "💌<b>Сообщение отправленно</b>", reply_markup=back_to_main_menu)
    await state.finish()
    await state.update_data(username=username)


# ===============ADD/CHANGE ACCOUNT===========
@dp.callback_query_handler(text="add_account")
async def show_all_chats(call: CallbackQuery, state: FSMContext):
    msg_to_edit = await call.message.edit_text("<b>Напишите номер аккаунта. В формате +7987678990</b>",
                                               reply_markup=back_to_main_menu)
    await AddAccount.A1.set()
    await state.update_data(msg_to_edit=msg_to_edit)


@dp.message_handler(state=AddAccount.A1)
async def receive_number(message: Message, state: FSMContext):
    data = await state.get_data()
    msg_to_edit = data.get("msg_to_edit")
    number = message.text
    await message.delete()
    if os.path.exists(f"sessions/{number}.session"):
        os.remove(f"sessions/{number}.session")
        await update_session(number, None)
        await del_all_chats(number)
    client = TelegramClient(f"sessions/{number}", api_id, api_hash)
    await client.connect()
    sent = await client.send_code_request(phone=number)
    await client.disconnect()
    await msg_to_edit.edit_text(f"<b>Вы указали <code>{number}</code>\n"
                                f"Укажите первую цифру кода:</b>",
                                reply_markup=code_menu)
    await AddAccount.next()
    await state.update_data(number=number, sent=sent, code_hash=sent.phone_code_hash)


@dp.callback_query_handler(text_startswith="code_number:", state=AddAccount.A2)
async def receive_code(call: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    msg_to_edit = data.get("msg_to_edit")
    num_1 = call.data.split(":")[1]
    await msg_to_edit.edit_text(f"<b>Код будет выстраиваться тут: <code>{num_1}</code></b>", reply_markup=code_menu)
    await AddAccount.next()
    await state.update_data(num_1=num_1)


@dp.callback_query_handler(text_startswith="code_number:", state=AddAccount.A3)
async def receive_code(call: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    msg_to_edit, num_1 = data.get("msg_to_edit"), data.get("num_1")
    num_2 = call.data.split(":")[1]
    code = num_1 + num_2
    await msg_to_edit.edit_text(f"<b>Код будет выстраиваться тут: <code>{code}</code></b>", reply_markup=code_menu)
    await AddAccount.next()
    await state.update_data(num_2=num_2)


@dp.callback_query_handler(text_startswith="code_number:", state=AddAccount.A4)
async def receive_code(call: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    msg_to_edit, num_1, num_2 = data.get("msg_to_edit"), data.get("num_1"), data.get("num_2")
    num_3 = call.data.split(":")[1]
    code = num_1 + num_2 + num_3
    await msg_to_edit.edit_text(f"<b>Код будет выстраиваться тут: <code>{code}</code></b>", reply_markup=code_menu)
    await AddAccount.next()
    await state.update_data(num_3=num_3)


@dp.callback_query_handler(text_startswith="code_number:", state=AddAccount.A5)
async def receive_code(call: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    msg_to_edit, num_1, num_2, num_3 = data.get("msg_to_edit"), data.get("num_1"), data.get("num_2"), data.get("num_3")
    num_4 = call.data.split(":")[1]
    code = num_1 + num_2 + num_3 + num_4
    await msg_to_edit.edit_text(f"<b>Код будет выстраиваться тут: <code>{code}</code></b>", reply_markup=code_menu)
    await AddAccount.next()
    await state.update_data(num_4=num_4)


@dp.callback_query_handler(state=AddAccount.A6)
async def receive_code(call: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    msg_to_edit, num_1, num_2, num_3 = data.get("msg_to_edit"), data.get("num_1"), data.get("num_2"), data.get("num_3")
    number, num_4, sent, code_hash = data.get("number"), data.get("num_4"), data.get("sent"), data.get("code_hash")
    num_5 = call.data.split(":")[1]
    code = num_1 + num_2 + num_3 + num_4 + num_5
    try:
        client = TelegramClient(f"sessions/{number}", api_id, api_hash)
        await client.connect()
        await client.sign_in(phone=number, code=code, phone_code_hash=code_hash)
        await client.disconnect()
        await update_session(call.from_user.id, call.from_user.id)
        await add_acc(call.from_user.id, number)
        await msg_to_edit.edit_text(f"<b>Готово, аккаунт добавлен</b>", reply_markup=back_to_main_menu)
        await state.finish()
    except Exception as e:
        print(e)
        await msg_to_edit.edit_text("Не верный код. Попробуйте заново.", reply_markup=back_to_main_menu)
        await state.finish()
