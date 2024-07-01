from lib.session_kontrol2 import get_session_list, get_this_session
from concurrent.futures import ThreadPoolExecutor, as_completed
from colorama import init, Fore

init(autoreset=True)

async def check_user_sessions():
    success_color = Fore.LIGHTGREEN_EX
    white_color = Fore.WHITE
    cyan_color = Fore.CYAN
    yellow_color = Fore.YELLOW
    red_color = Fore.RED

    user_phone_numbers = await get_session_list()
    user_sessions = []

    print(success_color + f"\nTelebar Yazılımında Şuan {len(user_phone_numbers)} hesap bulunuyor.\n")

    perform_spam_check = input(yellow_color + "Hesapları spam kontrolünden geçirmek ister misiniz? (E/h): ").lower() != "h"
    print()

    online_count, banned_count, spam_count = 0, 0, 0

    with ThreadPoolExecutor() as executor:
        tasks = [executor.submit(get_this_session, phone_number, perform_spam_check) for phone_number in user_phone_numbers]

        for task in as_completed(tasks):
            session_info = await task.result()

            if not session_info.get("error"):
                user_sessions.append(session_info)
                print(success_color + f" [+] Sorunsuz: {session_info['phone']} | {session_info['first_name']} {session_info['last_name']} | {session_info['username']}")
                online_count += 1
            elif session_info["error"] == "ban":
                print(red_color + f" [-] Ban Yemiş: {session_info['phone']}")
                banned_count += 1
            elif session_info["error"] == "spam":
                print(cyan_color + f" [!!] Spam Yemiş: {session_info['phone']}[/]\t|[/] [!?] Bitecek Tarih: : {session_info['until']}")
                spam_count += 1

    print(yellow_color + f"\nYazılımdaki Sorunsuz Hesap Sayısı: {online_count}")

    if banned_count > 0:
        print(red_color + f"Toplam Banlı Hesaplar: {banned_count}")

    if spam_count > 0:
        print(cyan_color + f"Toplam Spamlı Hesaplar: {spam_count}")

    return user_sessions

# Fonksiyonu çağırarak kullanabilirsiniz
# sessions = await check_user_sessions()
