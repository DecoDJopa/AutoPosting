from datetime import datetime, timedelta

from aiogram.dispatcher import FSMContext
from aiogram.types import CallbackQuery

from data.config import month_dict, ADMINS
from keyboards.inline.menu import back_to_main_menu, check_menu, month_amount_menu
from loader import dp, bot
from states.states import BuyAccess
from utils.db_api.db_commands import select_user, delete_stat, update_date
from utils.qiwi import check_payment


@dp.callback_query_handler(text_startswith="buy_access")
async def add_balance_main(call: CallbackQuery, state: FSMContext):
    msg_to_edt = await call.message.edit_text("Выберите срок, на который хотите приобрести подписку👇",
                                              reply_markup=month_amount_menu)
    await BuyAccess.BS1.set()
    await state.update_data(msg_to_edt=msg_to_edt)


@dp.callback_query_handler(state=BuyAccess.BS1, text_startswith="month:")
async def add_balance_2(call: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    msg_to_edt = data.get("msg_to_edt")
    amount = call.data.split(":")[1]
    cost = month_dict.get(amount)
    keyboard, bill_id = await check_menu(cost, call.from_user.id, datetime.now() + timedelta(minutes=10))
    await msg_to_edt.edit_text("👇Оплатить подписку вы можете по ссылке ниже 👇 \n\n"
                               "💡Просто нажмите на соответствующую кнопку💡\n\n"
                               "⏳Счёт действителен 10 минут⏳",
                               reply_markup=keyboard)
    await state.update_data(bill_id=bill_id, amount=amount)
    await BuyAccess.next()


@dp.callback_query_handler(text="check", state=BuyAccess.BS2)
async def add_balance_main(call: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    bill_id, amount = data.get("bill_id"), data.get("amount")
    if await check_payment(bill_id):
        user = await select_user(call.from_user.id)
        date_list = user[3].split(" ")
        date_list = [int(num) for num in date_list]
        user_date = datetime(date_list[0], date_list[1], date_list[2], date_list[3], date_list[4])
        user_time = user_date - datetime.now()
        date_when_expires = datetime.now() + timedelta(hours=int(amount) * 30 * 24) + user_time
        date_to_db = str(date_when_expires).split(".")[0].replace("-", " ").split(":")
        date_to_db = " ".join(date_to_db[:-1])
        await update_date(call.from_user.id, date_to_db)
        if amount == "1":
            text = "1 месяц"
        elif amount == "3":
            text = "3 месяца"
        else:
            text = "6 месяцев"
        await bot.send_message(ADMINS[0], f"💸 Пользователь @{call.from_user.username} | "
                                          f"{call.from_user.id} купил подписку на {text}")
        await call.message.edit_text(f"🎉Поздравляю, вы купили подписку на {text}",
                                     reply_markup=back_to_main_menu)
        await state.finish()
    else:
        await call.answer("❗️Оплата не найдена")
