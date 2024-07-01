from telethon import TelegramClient, functions, types
import asyncio
from random import choice
from os import listdir

async def send_message(session, message, msgid, target_entity):
    try:
        client = TelegramClient("sessions/" + session, "2462520", "e073b57a2a0541608c3f1373bf22ea09")
        await client.start()

        message_obj = await client.get_messages(target_entity, ids=int(msgid))

        await client.send_message(target_entity, message=message, reply_to=message_obj.id)

    except Exception as e:
        print(f"HATA: {e}")

async def send_messages(messages: list, accounts: list, count: int, target_entity):
    print("Hesapların göndereceği mesajları lib/config/mesaj.txt dosyasına yazınız...")
    msgid = input("Mesaj id           : ")
    sure = input("kaç saniye beklensin: ")

    for i in range(count):
        session = choice(accounts)
        message = choice(messages)

        messages.remove(message)
        accounts.remove(session)

        await send_message(session, message, msgid, target_entity)
        await asyncio.sleep(int(sure))

async def uyecek():
    yorum = input("Kaç adet yollansın : ")

    sess = []
    for i in listdir("sessions"):
        if i.endswith(".session"):
            sess.append(i)

    target_entity_username = input("@ olmadan grup giriniz örn:[deneme01]: ")
    target_entity = await client.get_entity(target_entity_username)

    await send_messages([i.replace("\n", "") for i in open('lib/config/mesaj.txt', "r", encoding="utf-8").readlines()], sess, int(yorum), target_entity)

if __name__ == "__main__":
    asyncio.run(uyecek())
