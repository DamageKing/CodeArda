from telethon import TelegramClient
from telethon.errors import SessionPasswordNeededError
from telethon.tl.functions.account import GetPasswordRequest
from colorama import init, Fore
import os
import secrets

async def telegram_login():
    try:
        init()
        success_color = Fore.LIGHTGREEN_EX
        error_color = Fore.RED
        white_color = Fore.WHITE
        cyan_color = Fore.CYAN
        yellow_color = Fore.YELLOW
        reset_color = Fore.RESET

        while True:
            print(f"{error_color}\nTelegram Oturum Açma\n")

            api_id = input(f"{yellow_color}API ID girin (Varsayılan için 'w' basın): {error_color}")
            if api_id=='w':
                api_id = ("12553173")
            api_hash = input(f"{yellow_color}API Hash girin (Varsayılan için 'w' basın): {error_color}")
            if api_hash=='w':
                api_hash = str("98528f7b9b50a90535c736120a46e073")
            phone_number = input(f"{yellow_color}Telefon Numarası (+xxxx): {cyan_color}").replace(' ', '')

            if not api_id or not api_hash or not phone_number:
                print(f"{error_color}Hatalı giriş! API ID, API Hash ve Telefon Numarası zorunlu.")
                continue

            session_path = f"sessions/{phone_number}.session"

            try:
                print(f"{cyan_color}Telegram ile bağlantı kuruluyor...")
                client = TelegramClient(session_path, api_id, api_hash)
                await client.connect()
                print(f"{success_color}Bağlantı başarılı!\n")
            except Exception as e:
                print(f"{error_color}Bağlantı Hatası: {e}\n")
                continue

            if not await client.is_user_authorized():
                try:
                    print(f"{cyan_color}Doğrulama kodu gönderiliyor...")
                    await client.send_code_request(phone_number)
                    print(f"{success_color}Doğrulama kodu gönderildi. Lütfen kontrol edin!\n")
                except Exception as e:
                    print(f"{error_color}Doğrulama Kodu Gönderme Hatası: {e}\n")
                    continue

            try:
                verification_code = input('\nDoğrulama Kodu: ')
                print(f"{cyan_color}Doğrulama yapılıyor...")
                await client.sign_in(phone_number, verification_code)
                print(f"{success_color}Doğrulama başarılı!\n")
            except SessionPasswordNeededError:
                get_password_request = await client(GetPasswordRequest())
                two_factor_password = input(f'\n{success_color}İki Faktörlü Kimlik Doğrulama Şifresi ({get_password_request.hint}): ')
                print(f"{cyan_color}Doğrulama yapılıyor...")
                await client.sign_in(password=two_factor_password)
                print(f"{success_color}Doğrulama başarılı!\n")
            except Exception as e:
                print(f"{error_color}Doğrulama Hatası: {e}\n")
                continue

            user_info = {}

            async def get_user_info():
                user = await client.get_me()
                user_info['username'] = f"@{user.username}"
                user_info['full_name'] = f"{user.first_name} {user.last_name}"
                user_info['user_id'] = user.id
                print(f"{cyan_color}Bilgileriniz alınıyor...")
                await client.send_message('me', f"__Hey, **TELEBOT** yazılımına sorunsuz giriş yaptınız!__\n\n__Bilgileriniz;__\n\n**ID :** `{api_id}`\n**Hash :** `{api_hash}`\n**Telefon :** `{phone_number}`\n\n**Kendi güvenliğiniz için bu bilgileri kimseyle paylaşmayın.**")
                print(f"{success_color}Bilgileriniz alındı!\n")

            await get_user_info()

            await client.disconnect()

            print(f'{success_color}{phone_number} Session Kaydedildi..!\n')

            add_another_account = input(f'\nYeni hesap eklemek ister misiniz? [y/n]: ')
            if add_another_account.lower() != 'y':
                break

    except Exception as e:
        os.unlink(session_path)
        print(f"{error_color}Hata: {e}\n")

# Bu kısmı kullanarak fonksiyonu çağırabilirsiniz
# await telegram_login()
