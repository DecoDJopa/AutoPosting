from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from data.config import *


# =========================================================
# ========================MAIN MENU========================
from utils.db_api.db_commands import select_user_chats, select_user_accounts


def main_menu(account, user_id):
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text="⏳ Автопостинг",
                                     callback_data="all_accounts")
            ],
            [
                InlineKeyboardButton(text="🖥 Профиль", callback_data="personal_acc"),
                InlineKeyboardButton(text="📒Инфо", callback_data="inf")
            ],
            [
                InlineKeyboardButton(text="💌Отправить сообщение", callback_data="send_message")
            ],
            [
                InlineKeyboardButton(text="👑 Админ панель", callback_data="back_admin")
            ] if str(user_id) in ADMINS else []
        ]
    )
    return keyboard


# ========================PERSONAL ACCOUNT========================
# MAIN PERSONAL ACCOUNT MENU
personal_menu = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text="📥Пополнить баланс📥", callback_data="deposit")
        ],
        [
            InlineKeyboardButton(text="📖Все заказы", callback_data="my_orders"),
            InlineKeyboardButton(text="📖Статус заказа", callback_data="show_order_status")
        ],
        [
            InlineKeyboardButton(text="🔙Назад", callback_data="back_to_main_menu")
        ]
    ]
)


code_menu = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text="0️⃣", callback_data="code_number:0"),
            InlineKeyboardButton(text="1️⃣", callback_data="code_number:1"),
            InlineKeyboardButton(text="2️⃣", callback_data="code_number:2")
        ],
        [
            InlineKeyboardButton(text="3️⃣", callback_data="code_number:3"),
            InlineKeyboardButton(text="4️⃣", callback_data="code_number:4"),
            InlineKeyboardButton(text="5️⃣", callback_data="code_number:5")
        ],
        [
            InlineKeyboardButton(text="6️⃣", callback_data="code_number:6"),
            InlineKeyboardButton(text="7️⃣", callback_data="code_number:7"),
            InlineKeyboardButton(text="8️⃣", callback_data="code_number:8"),
        ],
        [
            InlineKeyboardButton(text="9️⃣", callback_data="code_number:9")
        ],
        [
            InlineKeyboardButton(text="🔙Назад", callback_data="back_to_main_menu")
        ]
    ]
)

# SHOW MY ORDERS MENU
my_orders_menu = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text="🔙Назад", callback_data="personal_acc")
        ]
    ]
)

# =========================================================
# ========================ADMIN MENU========================
# MAIN ADMIN MENU
admin_menu = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text="📮Рассылка", callback_data="broadcast")
        ],
        [
            InlineKeyboardButton(text="✅Выдать доступ", callback_data="give_time"),
            InlineKeyboardButton(text="⛔️Забрать доступ", callback_data="take_time")
        ],
        [
            InlineKeyboardButton(text="🔙В главное меню", callback_data="back_to_main_menu")
        ]
    ]
)

# BACK TO ADMIN MENU BUTTON
back_admin = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text="⬅️Назад", callback_data="back_admin")
        ]
    ]
)

# DELETE BROADCAST MESSAGE
broadcast_menu = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text="❇️Понял❇️", callback_data="delete_this_message")
        ]
    ]
)

# BROADCAST CONFIRM MENU
choose_menu = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text="✅Да", callback_data="broadcast:yes")
        ],
        [
            InlineKeyboardButton(text="❌Нет", callback_data="broadcast:no")
        ]
    ]
)

# ========================BACK TO MAIN MENU BUTTON========================
back_to_main_menu = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text="⬅️Назад", callback_data="back_to_main_menu")
        ]
    ]
)


# ========================CHATS MENU========================
# ALL USER CHATS
async def all_chats_menu(user_id, number):
    chats = await select_user_chats(user_id, number)
    keyboard = InlineKeyboardMarkup(row_width=2)
    for chat in chats:
        keyboard.insert(InlineKeyboardButton(text=chat[1], callback_data=f"uc::{chat[8]}"))
    keyboard.add(InlineKeyboardButton(text="➕Добавить чат", callback_data=f"add_new_chat:{number}"))
    keyboard.insert(InlineKeyboardButton(text="🗑Удалить аккаунт", callback_data=f"del_acc:{number}"))
    keyboard.add(InlineKeyboardButton(text="📜Загрузить чаты", callback_data=f"import_chats:{number}"))
    keyboard.insert(InlineKeyboardButton(text="⚙️Мульти-настройка", callback_data=f"multi_settings:{number}"))
    keyboard.add(InlineKeyboardButton(text="🔙Назад", callback_data=f"back_to_main_menu"))
    return keyboard


# ========================CHATS MENU========================
# ALL USER CHATS
async def accounts_menu(user_id):
    accs = await select_user_accounts(user_id)
    keyboard = InlineKeyboardMarkup(row_width=2)
    for acc in accs:
        keyboard.insert(InlineKeyboardButton(text=acc[1], callback_data=f"accounts:{acc[1]}"))
    keyboard.add(InlineKeyboardButton(text="➕ Добавить аккаунт", callback_data="add_account"))
    keyboard.add(InlineKeyboardButton(text="🔙Назад", callback_data=f"back_to_main_menu"))
    return keyboard


def multi_settings_menu(number):
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text="📝Изменить текст🔰", callback_data=f"multi`text`{number}"),
                InlineKeyboardButton(text="📝Изменить фото", callback_data=f"multi`photo`{number}")
            ],
            [
                InlineKeyboardButton(text="Включить все", callback_data=f"multi`turn_on`{number}"),
                InlineKeyboardButton(text="Выключить все", callback_data=f"multi`turn_off`{number}")
            ],
            [
                InlineKeyboardButton(text="🗑Удалить все", callback_data=f"multi`del`{number}")
            ],
            [
                InlineKeyboardButton(text="⬅️Назад", callback_data=f"accounts:{number}")
            ]
        ]
    )
    return keyboard


# INSIDE CHAT
def in_chat_menu(is_on, chat_id, number):
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text="📝Изменить текст🔰", callback_data=f"ed`text`{chat_id}"),
                InlineKeyboardButton(text="📝Изменить задержку", callback_data=f"ed`delay`{chat_id}")
            ],
            [
                InlineKeyboardButton(text="📝Изменить фото", callback_data=f"ed`photo`{chat_id}"),
                InlineKeyboardButton(text="🗑Удалить", callback_data=f"ed`del`{chat_id}")
            ],
            [
                InlineKeyboardButton(text="🔕Рассылка выключена" if is_on == 0 else "🔔Рассылка включена",
                                     callback_data=f"ed`turn`{chat_id}")
            ],
            [
                InlineKeyboardButton(text="⬅️Назад", callback_data=f"accounts:{number}")
            ]
        ]
    )
    return keyboard
