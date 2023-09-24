from datetime import datetime

from aiogram.types import Message, CallbackQuery

from keyboards.inline.menu import back_to_main_menu
from loader import dp, bot
from utils.db_api.db_commands import select_user


# ========================SHOW USER CABINET========================
@dp.callback_query_handler(text="personal_acc")
async def personal_acc(call: CallbackQuery):
    bot_info = await bot.get_me()
    user = await select_user(call.from_user.id)
    now_date = datetime.now()
    if user[3]:
        date_list = user[3].split(" ")
        date_list = list(map(int, date_list))
        date_when_expired = datetime(date_list[0], date_list[1], date_list[2], date_list[3], date_list[4])
        result_date = str(date_when_expired - now_date).split(".")[0].replace("days", "дня/дней").replace("day", "день")
    else:
        result_date = "00:00"
    await call.message.edit_text(f"<b>🖥 Профиль\n\n"
                                 f"🆔Ваш ID: <code>{call.from_user.id}</code>\n"
                                 f"🧿Ваша подписка продлится еще:</b> "
                                 f"<code>{result_date}</code>",
                                 reply_markup=back_to_main_menu)
