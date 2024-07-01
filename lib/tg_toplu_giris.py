from telethon import TelegramClient
from telethon.errors import SessionPasswordNeededError
from telethon.tl.functions.account import GetPasswordRequest
from colorama import init, Fore
from os import remove

async def tg2():
    try:
        init()
        success_color = Fore.LIGHTGREEN_EX
        white_color = Fore.WHITE
        cyan_color = Fore.CYAN
        yellow_color = Fore.YELLOW
        red_color = Fore.RED
        reset_color = Fore.RESET

        while True: 
            api_id = "12553173"
            api_hash = "98528f7b9b50a90535c736120a46e073"
            phone_number = input(f'{yellow_color}Telefon Numarası (+xxxx): {red_color}').replace(' ', '')
            session_path = f"sessions/{phone_number}.session"

            try:
                client = TelegramClient(session_path, api_id, api_hash)
                await client.connect()
            except Exception as error:
                remove(session_path)
                print(error)

            if not await client.is_user_authorized():
                try:
                    await client.send_code_request(phone_number)
                except Exception as error:
                    remove(session_path)
                    print(error)

            try:
                verification_code = input('\nDoğrulama Kodu: ')
                await client.sign_in(phone_number, verification_code)
            except SessionPasswordNeededError:
                get_password_request = await client(GetPasswordRequest())
                await client.sign_in(password=input(f'\n2 Adımlı Doğrulama/ İpucu ({get_password_request.hint}): '))
            except Exception as error:
                remove(session_path)
                print(error)

            user_info = {}

            async def get_user_info():
                user = await client.get_me()

                user_info['username'] = f"@{user.username}"
                user_info['full_name'] = f"{user.first_name} {user.last_name}"
                user_info['user_id'] = user.id
                await client.send_message('me', f"__Hey, **TELEBOT** yazılımına sorunsuz giriş yaptınız!__\n\n__Bilgileriniz;__\n\n**ID :** `{api_id}`\n**Hash :** `{api_hash}`\n**Telefon :** `{phone_number}`\n\n**Kendi güvenliğiniz için bu bilgileri kimseyle paylaşmayın.**")
                
            await get_user_info()

            await client.disconnect()

            print(success_color + f'{phone_number} Session Kaydedildi..!')

            add_another_account = input(f'\nYeni hesap eklemek ister misiniz? [y/n]: ')
            if 'y' in add_another_account.lower():
                pass
            else:
                input(f'\n{success_color}Ana menüye gitmek için enter a basın...')
                break

    except Exception as error:
        remove(session_path)
        print(error)

# Bu kısmı kullanarak fonksiyonu çağırabilirsiniz
# await telegram_login()
