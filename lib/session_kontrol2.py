from telethon import TelegramClient
from telethon.sessions import StringSession
from os import listdir, remove, makedirs
from telethon.errors.rpcerrorlist import AuthKeyDuplicatedError, AuthKeyUnregisteredError, UserDeactivatedBanError, FloodWaitError
import asyncio
import random
from sqlite3 import OperationalError, DatabaseError
from shutil import move
from telethon.tl.functions.messages import StartBotRequest
from re import search

re_until_date = lambda spam_message: search(r"(\d\d? [a-zA-z]+ \d{4}, \d{2}:\d{2} UTC)", spam_message)

TG_API_ID = "12553173"
TG_API_HASH = "98528f7b9b50a90535c736120a46e073"
SESSIONS_PATH = "sessions/"
BAN_PATH = f"{SESSIONS_PATH}Banlanan/"
SPAM_PATH = f"{SESSIONS_PATH}Spam/"
UNTIL_PATH = f"{SPAM_PATH}Until/"
PERSIST_PATH = f"{SPAM_PATH}Persist/"
SPAM_BOT_USERNAME = "@SpamBot"

async def get_session_list() -> list:
    return [file.replace('.session', '') for file in listdir(SESSIONS_PATH) if file.endswith(".session")]

async def get_this_session(phone_number, check_spam: bool = False) -> dict:
    session_loop = asyncio.get_event_loop()
    session_file_path = f'{SESSIONS_PATH}{phone_number}.session'
    client = TelegramClient(session_file_path, TG_API_ID, TG_API_HASH, loop=session_loop)

    try:
        await client.connect()
    except (AuthKeyDuplicatedError, OperationalError, AuthKeyUnregisteredError, DatabaseError):
        await client.disconnect()
        await asyncio.sleep(random.uniform(1, 3))
        remove(session_file_path)
        client = TelegramClient(session_file_path, TG_API_ID, TG_API_HASH, loop=session_loop)
        await client.connect()

    user_info = await client.get_me()

    if not user_info:
        await client.disconnect()
        await asyncio.sleep(random.uniform(1, 3))
        move(session_file_path, f'{BAN_PATH}{phone_number}.session')
        return {"phone": phone_number, "error": "ban"}

    if check_spam:
        try:
            await client(StartBotRequest(
                bot=SPAM_BOT_USERNAME,
                peer=SPAM_BOT_USERNAME,
                start_param="SpamCheck"
            ))

            await asyncio.sleep(1)

            last_message_obj = await client.get_messages(SPAM_BOT_USERNAME, 1)
            last_message = last_message_obj[0]
            last_message_text = last_message.message
        except UserDeactivatedBanError:
            await client.disconnect()
            await asyncio.sleep(random.uniform(1, 3))
            move(session_file_path, f'{BAN_PATH}{phone_number}.session')
            return {"phone": phone_number, "error": "ban"}
        except FloodWaitError as flood:
            await client.disconnect()
            await asyncio.sleep(random.uniform(1, 3))
            move(session_file_path, f'{UNTIL_PATH}{phone_number}.session')
            return {"phone": phone_number, "error": "spam", "until": f"{flood.seconds} FloodWait"}

    string_session = str(StringSession.save(client.session))

    await client.disconnect()

    if check_spam and (not last_message_text.startswith("Good news") or last_message_text.startswith("/start")):
        until_date = re_until_date(last_message_text)
        target_folder = UNTIL_PATH if until_date else PERSIST_PATH
        move(session_file_path, f'{target_folder}{phone_number}.session')
        until_str = until_date.group(1) if until_date else "~"
        return {"phone": phone_number, "error": "spam", "until": until_str}

    return {
        "client": client,
        "string": string_session,
        "user_id": user_info.id,
        "phone": f"+{user_info.phone}",
        "first_name": user_info.first_name,
        "last_name": user_info.last_name,
        "username": f"@{user_info.username}",
    }