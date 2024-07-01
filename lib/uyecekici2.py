from lib.kanalcek import give_chat_id
from telethon.tl.functions.channels import GetParticipantsRequest
from telethon.tl.types import ChannelParticipantsSearch, UserStatusOnline, UserStatusOffline, UserStatusRecently, UserStatusLastWeek, UserStatusLastMonth
from datetime import datetime, timedelta
from colorama import init, Fore

lg = Fore.LIGHTGREEN_EX
w = Fore.WHITE
cy = Fore.CYAN
ye = Fore.YELLOW
k = Fore.RED
n = Fore.RESET
colors = [lg, k, w, cy, ye]

async def get_this_group_members(session, group, filter=None):

    today = datetime.now().date()
    group_id = await give_chat_id(session['client'], group)

    users = []

    alphabet = tuple(chr(letter) for letter in range(ord("a"), ord("z") + 1))
    limit = 200

    for letter in alphabet:
        participants = await session['client'](GetParticipantsRequest(
            channel=group_id,
            filter=ChannelParticipantsSearch(letter),
            offset=0,
            limit=limit,
            hash=0
        ))

        for user in participants.users:
            if not (user.username and not user.bot and not user.scam and not user.deleted):
                continue

            user_status = user.status
            user_date = today

            if isinstance(user_status, (UserStatusOnline, UserStatusOffline, UserStatusRecently, UserStatusLastWeek, UserStatusLastMonth)):
                if isinstance(user_status, UserStatusOnline):
                    user_date = datetime(user_status.expires.year, user_status.expires.month, user_status.expires.day).date()

                if isinstance(user_status, UserStatusOffline):
                    user_date = datetime(user_status.was_online.year, user_status.was_online.month, user_status.was_online.day).date()

            if filter:
                if (today - user_date).days <= 1:
                    users.append({
                        'id': user.id,
                        'nick': f'@{user.username}' if user.username else None,
                        'ad': user.first_name or None,
                        'soyad': user.last_name or None,
                    })
            else:
                users.append({
                    'id': user.id,
                    'nick': f'@{user.username}' if user.username else None,
                    'ad': user.first_name or None,
                    'soyad': user.last_name or None,
                })

    sorted_users = sorted(users, key=lambda user_dict: user_dict['id'])

    print(lg+f"[+] - {len(sorted_users)} Adet Kullanıcı Çekildi » {group}")
    return sorted_users
