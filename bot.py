from aiogram.utils import executor

from loader import scheduler, dp
from utils.db_api.db_commands import select_all_chats
import middlewares, filters, handlers
from utils.notify_admins import on_startup_notify
from utils.other_utils import send_message_to_chat


async def restore_jobs():
    chats = await select_all_chats()
    for chat in chats:
        if chat[6] == 1:
            scheduler.add_job(
                send_message_to_chat,
                "interval", minutes=chat[3],
                args=(chat[0], chat[2], chat[8]),
                id=f"{chat[0]}:{chat[8]}"
            )


async def on_startup(dispatcher):
    await on_startup_notify(dispatcher)
    await restore_jobs()


if __name__ == '__main__':
    scheduler.start()
    executor.start_polling(dp, on_startup=on_startup)
