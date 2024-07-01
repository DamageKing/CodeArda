import os, asyncio
import sys
import random
from telethon.tl.functions.messages import GetDiscussionMessageRequest
from telethon import TelegramClient
from telethon.sessions import StringSession

import requests
import bs4
import pickle, pyfiglet
from colorama import init, Fore
from time import sleep
from os import listdir
from random import choice
import time

from lib.tg_grisi2 import telegram_login
from lib.tg_toplu_giris import tg2
from lib.session_kontrol import check_user_sessions
from lib.hesapsayi2 import trman
from lib.hesapsil import delete_accounts_async
from lib.uyecekici import grup_uyelerini_disa_aktar
from lib.memberekle import grup_uye_ekle

async def main():
    init()
    lg = Fore.LIGHTGREEN_EX
    w = Fore.WHITE
    cy = Fore.CYAN
    ye = Fore.YELLOW
    k = Fore.RED
    n = Fore.RESET

    def printSlow(text):
        for char in text:
            print(char, end="")
            sys.stdout.flush()
            time.sleep(.1)

    def Main_Program():
        printSlow("Erişim Sağlandı...")
        time.sleep(.1)

    if __name__ == "__main__":
        Main_Program()

    def banner():
        f = pyfiglet.Figlet(font='small')
        banner = f.renderText('TELEBAR')
        print(f'{ye}{banner}{n}Versiyon: 7.1 | Yapımcı: ArdaBarut')
        print("")

    lisans = input("Lisans Giriniz: ")
    r = requests.get('https://raw.githubusercontent.com/DamageKing/asdlaslc-mskldm/main/lisans.txt')
    if lisans in r.text:
        def clr():
            os.system('clear')

        while True:
            clr()
            banner()
            print(cy+'[1] Telegram Hesabına Giriş Yap'+n)
            print(cy+"[2] Telegram Hesaplarına Toplu Şekilde Giriş Yap!"+n)
            print(cy+'[3] Session dosyaları ile Telegram Hesaplarını içeri aktar!'+n)
            print(cy+'[4] Hesapları Kontrol Et (Spamlı, Banlı...)'+n)
            print(cy+'[5] Sorunsuz Hesapların Hepsini Listele!'+n)
            print(cy+'[6] Hesap Silme Menüsü'+n)
            print(cy+'[7] Yorum Botu'+n)
            print('')
            print(ye+"[8] Hedef Gruptan Üye Çekme Sistemi")
            print(ye+"[9] Gruba Üye Ekleme Sistemi")
            print('')
            print(k+'[10] Çık')
            a = int(input(lg+f'\nSeçiniz: {k}'))
            if a == 1:
                try:
                    await telegram_login()
                    input(f'\n{lg}Ana menüye gitmek için enter a basın...')
                except Exception as err:
                    print(err)
            elif a == 2:
                try:
                    await tg2()
                except Exception as err:
                    print(err)
            if a == 3:
                clr()
                banner()
                print(ye+"Session dosyalarınızı 'sessions' klasörüne atmanız yeterli!  Artık ek bir işlem beklemeye gerek yok!")
                input(f'\n{lg}Ana menüye gitmek için enter a basın...')
            elif a == 4:
                try:
                    await check_user_sessions()
                    input(f'\n{lg}Ana menüye gitmek için enter a basın...')
                except Exception as err:
                    print(err)
            elif a == 5:
                try:
                    await trman()
                except Exception as err:
                    print(err)
                input(f'\n{lg}Ana menüye gitmek için enter a basın...')
            elif a == 6:
                try:
                    await delete_accounts_async()
                except Exception as err:
                    print(err)
            elif a == 7:
                from lib.yorum import send_messages
            elif a == 8:
                try:
                    await grup_uyelerini_disa_aktar()
                except Exception as err:
                    print(err)
                    time.sleep(2)
            elif a == 9:
                group = input("Eklenecek Grup Linki : ")
                ses_by_add = int(input("Her Hesaptan Kaç Üye Eklenmeli? : "))
                delay_min = int(input("Her Üye Eklemeye Yönelik Minimum Gecikme : "))
                delay_maks = int(input("Her Üye Eklemeye Yönelik Maksimum Gecikme : "))

                try:
                    await grup_uye_ekle(group, ses_by_add, [delay_min, delay_maks])
                except Exception as err:
                    print(err)
            if a == 10:
                clr()
                banner()
                quit()
    else:
        print("LİSANS GEÇERSİZ!!")

try:
    asyncio.run(main())
except Exception as err:
    print(err)