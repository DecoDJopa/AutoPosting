import aiosqlite


# ========================USERS========================
async def add_user(user_id):
    conn = await aiosqlite.connect('db.db', check_same_thread=False)
    await conn.execute("INSERT INTO users (user_id) VALUES(?)", (user_id,))
    await conn.commit()
    await conn.close()


async def select_all_users():
    conn = await aiosqlite.connect('db.db', check_same_thread=False)
    cursor = await conn.execute(f"SELECT * FROM users")
    h = await cursor.fetchall()
    await conn.close()
    return h


async def select_user(user_id):
    conn = await aiosqlite.connect('db.db', check_same_thread=False)
    cursor = await conn.execute(f"SELECT * FROM users WHERE user_id=?", (user_id,))
    h = await cursor.fetchone()
    await conn.close()
    return h


async def update_date(user_id, date):
    conn = await aiosqlite.connect('db.db', check_same_thread=False)
    await conn.execute("UPDATE users SET access_expired=? WHERE user_id=?", (date, user_id))
    await conn.commit()
    await conn.close()


async def update_session(user_id, session):
    conn = await aiosqlite.connect('db.db', check_same_thread=False)
    await conn.execute("UPDATE users SET telethon_session=? WHERE user_id=?", (session, user_id))
    await conn.commit()
    await conn.close()


async def del_user(user_id):
    conn = await aiosqlite.connect('db.db', check_same_thread=False)
    await conn.execute("DELETE FROM users WHERE user_id = ?", (user_id,))
    await conn.commit()
    await conn.close()


# ========================CHATS========================
async def add_chat(user_id, name, chat_url, chat_id, number):
    conn = await aiosqlite.connect('db.db', check_same_thread=False)
    await conn.execute("INSERT INTO chats (user_id, name, chat_url, chat_id, number) VALUES(?,?,?,?,?)",
                       (user_id, name, chat_url, chat_id, number))
    await conn.commit()
    await conn.close()


async def select_user_chats(user_id, number):
    conn = await aiosqlite.connect('db.db', check_same_thread=False)
    cursor = await conn.execute(f"SELECT * FROM chats WHERE user_id=? AND number=?", (user_id, number))
    h = await cursor.fetchall()
    await conn.close()
    return h


async def add_acc(user_id, number):
    conn = await aiosqlite.connect('db.db', check_same_thread=False)
    await conn.execute("INSERT INTO accounts (user_id, account_num) VALUES(?,?)",
                       (user_id, number))
    await conn.commit()
    await conn.close()


async def del_acc(user_id, number):
    conn = await aiosqlite.connect('db.db', check_same_thread=False)
    await conn.execute("DELETE FROM accounts WHERE user_id=? AND account_num=?",
                       (user_id, number))
    await conn.commit()
    await conn.close()


async def select_user_accounts(user_id):
    conn = await aiosqlite.connect('db.db', check_same_thread=False)
    cursor = await conn.execute(f"SELECT * FROM accounts WHERE user_id=?", (user_id,))
    h = await cursor.fetchall()
    await conn.close()
    return h


async def select_all_chats():
    conn = await aiosqlite.connect('db.db', check_same_thread=False)
    cursor = await conn.execute(f"SELECT * FROM chats")
    h = await cursor.fetchall()
    await conn.close()
    return h


async def select_chat(user_id, chat_id):
    conn = await aiosqlite.connect('db.db', check_same_thread=False)
    cursor = await conn.execute(f"SELECT * FROM chats WHERE user_id=? AND chat_id=?", (user_id, chat_id))
    h = await cursor.fetchone()
    await conn.close()
    return h


async def select_chat_num(number, chat_id):
    conn = await aiosqlite.connect('db.db', check_same_thread=False)
    cursor = await conn.execute(f"SELECT * FROM chats WHERE number=? AND chat_url=?", (number, chat_id))
    h = await cursor.fetchone()
    await conn.close()
    return h


async def check_delay(user_id, delay, number):
    conn = await aiosqlite.connect('db.db', check_same_thread=False)
    cursor = await conn.execute(f"SELECT * FROM chats WHERE user_id=? AND delay=? AND number=?",
                                (user_id, delay, number))
    h = await cursor.fetchone()
    await conn.close()
    return h


async def update_delay(user_id, chat_id, delay):
    conn = await aiosqlite.connect('db.db', check_same_thread=False)
    await conn.execute("UPDATE chats SET delay=? WHERE user_id=? AND chat_id=?", (delay, user_id, chat_id))
    await conn.commit()
    await conn.close()


async def update_text(user_id, chat_id, text):
    conn = await aiosqlite.connect('db.db', check_same_thread=False)
    await conn.execute("UPDATE chats SET msg_text=? WHERE user_id=? AND chat_id=?", (text, user_id, chat_id))
    await conn.commit()
    await conn.close()


async def update_all_text(number, text):
    conn = await aiosqlite.connect('db.db', check_same_thread=False)
    await conn.execute("UPDATE chats SET msg_text=? WHERE number=?", (text, number))
    await conn.commit()
    await conn.close()


async def update_pic(user_id, chat_id, pic):
    conn = await aiosqlite.connect('db.db', check_same_thread=False)
    await conn.execute("UPDATE chats SET picture=? WHERE user_id=? AND chat_id=?", (pic, user_id, chat_id))
    await conn.commit()
    await conn.close()


async def update_all_pic(number, pic):
    conn = await aiosqlite.connect('db.db', check_same_thread=False)
    await conn.execute("UPDATE chats SET picture=? WHERE number=?", (pic, number))
    await conn.commit()
    await conn.close()


async def del_chat(user_id, chat_id):
    conn = await aiosqlite.connect('db.db', check_same_thread=False)
    await conn.execute("DELETE FROM chats WHERE user_id=? AND chat_id=?", (user_id, chat_id))
    await conn.commit()
    await conn.close()


async def del_all_chats_number(number):
    conn = await aiosqlite.connect('db.db', check_same_thread=False)
    await conn.execute("DELETE FROM chats WHERE number=?", (number,))
    await conn.commit()
    await conn.close()


async def del_chats_by_num(user_id, number):
    conn = await aiosqlite.connect('db.db', check_same_thread=False)
    await conn.execute("DELETE FROM chats WHERE user_id=? AND number=?", (user_id, number))
    await conn.commit()
    await conn.close()


async def del_all_chats(user_id):
    conn = await aiosqlite.connect('db.db', check_same_thread=False)
    await conn.execute("DELETE FROM chats WHERE user_id=?", (user_id,))
    await conn.commit()
    await conn.close()


async def update_is_active(user_id, chat_id, is_active):
    conn = await aiosqlite.connect('db.db', check_same_thread=False)
    await conn.execute("UPDATE chats SET is_active=? WHERE user_id=? AND chat_id=?", (is_active, user_id, chat_id))
    await conn.commit()
    await conn.close()


async def set_not_active(user_id):
    conn = await aiosqlite.connect('db.db', check_same_thread=False)
    await conn.execute("UPDATE chats SET is_active=0 WHERE user_id=? ", (user_id,))
    await conn.commit()
    await conn.close()
