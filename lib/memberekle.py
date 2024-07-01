from telethon import TelegramClient
from telethon.tl.functions.account import UpdateStatusRequest
from telethon.tl.functions.channels import InviteToChannelRequest
from telethon.tl.types import PeerChannel
from telethon.errors import (
    FloodWaitError,
    UserDeactivatedBanError,
    PeerFloodError,
    UserPrivacyRestrictedError,
    UserNotMutualContactError,
    UserChannelsTooMuchError,
    ChannelInvalidError,
    UsernameNotOccupiedError,
    UserBannedInChannelError,
    ChatWriteForbiddenError,
)
from sqlite3 import OperationalError
from lib.session_kontrol import check_user_sessions
from lib.uyecekici2 import get_this_group_members
from lib.kanalcek import give_chat_id
from os.path import isfile
import json
import random
import time
from rich.console import Console
from colorama import init, Fore

lg = Fore.LIGHTGREEN_EX
w = Fore.WHITE
cy = Fore.CYAN
ye = Fore.YELLOW
k = Fore.RED
n = Fore.RESET
colors = [lg, k, w, cy, ye]

async def grup_uye_ekle(grup, DONGU_SAYISI: int, UYKU_SURESI: list):
    console = Console()

    if not isfile("lib/config/uyeler.json"):
        console.print(k + "\n\n[!] Önce Üyeleri Dışa Aktar!", justify="center", width=70)
        return

    oturumlar = await check_user_sessions()
    random.shuffle(oturumlar)
    var_olan_kisiler = []

    for oturum in oturumlar:
        client: TelegramClient = oturum['client']
        await client.connect()
        await client(UpdateStatusRequest(offline=False))

        try:
            grup_uyeleri = await get_this_group_members(oturum, grup, False)
            var_olan_kisiler.extend(uye['nick'] for uye in grup_uyeleri)
            console.log(cy + f"[+] [ {grup} ] Bu Grup Üyelerini Dışa Aktarmak İçin Giriş Yapılıyor » {oturum['phone']} «")
            console.log(f"[magenta][+] [ {grup} ] Mevcut » {len(var_olan_kisiler)} Aktif Üye «")
            break
        except Exception as hata:
            console.log(f"[red][!] [{type(hata).__name__}] | {grup} | {oturum['phone']}")
            continue

    random.shuffle(oturumlar)

    for oturum in oturumlar:
        client: TelegramClient = oturum['client']
        await client.connect()

        try:
            await give_chat_id(client, grup)
            console.log(f"[green][+] [ {grup} ] Giriş Başarılı » {oturum['phone']} «")
        except Exception as hata:
            console.log(f"[red][!] [{type(hata).__name__}] | {grup} | {oturum['phone']}")
            continue

    suser_nickleri = []

    with open('lib/config/uyeler.json', "r+", encoding='utf-8') as json_dosyasi:
        json_suserler = json.loads(json_dosyasi.read())
        try:
            suser_nickleri.extend(nick['nick'] for nick in json_suserler)
        except TypeError:
            suser_nickleri.extend(json_suserler)

    if not suser_nickleri:
        console.print("[yellow]Uyeler.json dosyasında hiç kullanıcı adı bulunamadı.")
        return

    oturum_sayisi = len(oturumlar)
    console.print(f'\n[cyan][~] - {oturum_sayisi} Adet - Hesabınız var..', justify="center", width=70)

    oturum_index = 0
    eklenen_suser_sayisi = 0
    dongu_sayisi = 1
    maks_dongu = (len(oturumlar) * DONGU_SAYISI)
    grup_entity = PeerChannel((await client.get_entity(grup)).id)

    for suser in suser_nickleri:
        if dongu_sayisi == maks_dongu:
            console.print(
                f"\n\n[yellow]{DONGU_SAYISI} Döngü Tamamlandı, Botu Durdurdum.\n\nToplam Eklenen : {eklenen_suser_sayisi} Kişi Oldu..",
                justify="center", width=70)
            with open('lib/config/uyeler.json', "w+") as cli_bitti:
                cli_bitti.write(json.dumps(suser_nickleri, ensure_ascii=False, sort_keys=False, indent=2))
            break

        rastgele = random.randrange(len(suser_nickleri))
        bilgi = suser_nickleri[rastgele]

        if oturum_sayisi == 0:
            console.print(f'[yellow]\n\nOturum Yok!!\n\nToplam Eklenen : {eklenen_suser_sayisi} Kişi Oldu..',
                          justify="center", width=70)
            with open('lib/config/uyeler.json', "w+") as cli_bitti:
                cli_bitti.write(json.dumps(suser_nickleri, ensure_ascii=False, sort_keys=False, indent=2))
            return

        if oturum_index == oturum_sayisi:
            oturum_index = 0

        if (not bilgi) or (bilgi in var_olan_kisiler):
            console.log(f"\n\n[yellow]{bilgi} Zaten Gruba Dahil..")
            suser_nickleri.remove(bilgi)
            continue

        uyku = lambda: time.sleep(random.uniform(UYKU_SURESI[0], UYKU_SURESI[1]))

        try:
            gecerli_oturum = oturumlar[oturum_index]
            await gecerli_oturum['client'].connect()
        except IndexError:
            client_index = 0
            continue

        try:
            eklenecek_suser = await gecerli_oturum['client'].get_input_entity(bilgi)
            console.log(f"\n\n[yellow][~] {gecerli_oturum['phone']} | {bilgi}\'i Eklemeyi Deniyorum..")
            await gecerli_oturum['client'](InviteToChannelRequest(grup_entity, [eklenecek_suser]))
            eklenen_suser_sayisi += 1
            console.log(f"[green][+] {bilgi}\'i Ekledim\t| Toplam Eklenen : {eklenen_suser_sayisi} Kişi Oldu..")
            suser_nickleri.remove(bilgi)
            oturum_index += 1
            uyku()
            continue
        except PeerFloodError as flood:
            console.log(f'[red][!] Hata Verdi | Floodlu Hesap.. » ({flood}) | {gecerli_oturum["phone"]} Düşürdüm...')
            oturumlar.remove(gecerli_oturum)
            await gecerli_oturum['client'].disconnect()
            oturum_index += 1
            console.log(f'\n\t[red][!] - {oturum_sayisi} Adet - Hesabınız Kaldı..!!')
            uyku()
            continue
        except UserDeactivatedBanError:
            console.log(f'[red][!] Hata Verdi | Ban Yedi | {gecerli_oturum["phone"]} Sildim..')
            oturumlar.remove(gecerli_oturum)
            await gecerli_oturum['client'].disconnect()
            oturum_index += 1
            console.log(f'\n\t[red][!] - {oturum_sayisi} Adet - Hesabınız Kaldı..!!')
            uyku()
            continue
        except (ChatWriteForbiddenError, ValueError):
            console.log(f'[red][!] Hata Verdi | (ChatWriteForbiddenError, ValueError) | {gecerli_oturum["phone"]} Sildim..')
            oturumlar.remove(gecerli_oturum)
            await gecerli_oturum['client'].disconnect()
            oturum_index += 1
            console.log(f'\n\t[red][!] - {oturum_sayisi} Adet - Hesabınız Kaldı..!!')
            uyku()
            continue
        except UserBannedInChannelError:
            console.log(f'[red][!] Hata Verdi | BAN YEDİ!!! | {gecerli_oturum["phone"]} Sildim..')
            oturumlar.remove(gecerli_oturum)
            await gecerli_oturum['client'].disconnect()
            oturum_index += 1
            console.log(f'\n\t[red][!] - {oturum_sayisi} Adet - Hesabınız Kaldı..!!')
            uyku()
            continue
        except UserPrivacyRestrictedError:
            console.log('[red][!] Hata Verdi | Gizlilik Ayarları..')
            suser_nickleri.remove(bilgi)
            oturum_index += 1
            uyku()
            continue
        except UserNotMutualContactError:
            console.log('[red][!] Kullanıcı Karşılıksız İletişim Hatası..')
            suser_nickleri.remove(bilgi)
            oturum_index += 1
            uyku()
            continue
        except UserChannelsTooMuchError:
            console.log('[red][!] Hata Verdi | Kullanıcı Çok Fazla Gruba Katılmış..')
            suser_nickleri.remove(bilgi)
            oturum_index += 1
            uyku()
            continue
        except ChannelInvalidError:
            console.log('[red][!] Hata Verdi | ChannelInvalidError')
            suser_nickleri.remove(bilgi)
            oturum_index += 1
            uyku()
            continue
        except UsernameNotOccupiedError:
            console.log('[red][!] Hata Verdi | UsernameNotOccupiedError')
            suser_nickleri.remove(bilgi)
            oturum_index += 1
            uyku()
            continue
        except FloodWaitError as fw:
            console.log(f"\t[red][!] Hata Verdi | ({fw}) | {bilgi}")
            fw_suresi = int(str(fw).split()[3])
            if fw_suresi > 500:
                oturumlar.remove(gecerli_oturum)
                await gecerli_oturum['client'].disconnect()
                console.log(f'\n\t[red][!] - {oturum_sayisi} Adet - Hesabınız Kaldı..!!')
            oturum_index += 1
            continue
        except OperationalError:
            console.log(
                f'[red][!] Takıldı | OperationalError | Oturum YOK | {gecerli_oturum["phone"]} Sildim..')
            oturumlar.remove(gecerli_oturum)
            await gecerli_oturum['client'].disconnect()
            oturum_index += 1
            console.log(f'\n\t[red][!] - {oturum_sayisi} Adet - Hesabınız Kaldı..!!')
            uyku()
            continue
        except Exception as hata:
            console.log(f"\t[red][!] Hata Verdi | ({type(hata).__name__}) | {hata}")
            oturum_index += 1
            continue
        finally:
            if dongu_sayisi % DONGU_SAYISI == 0:
                console.log(f"\n\n[magenta][✅] {dongu_sayisi / DONGU_SAYISI} İşlem Tamamdır ! [✅]\n")
            dongu_sayisi += 1

    console.print(
        f"\n\n[yellow]Json Dosyası Tamamlandı, Botu Durdurdum.\n\nToplam Eklenen : {eklenen_suser_sayisi} Kişi Oldu..",
        justify="center", width=70)

    with open('lib/config/uyeler.json', "w+") as cli_bitti:
        cli_bitti.write(json.dumps(suser_nickleri, ensure_ascii=False, sort_keys=False, indent=2))

# Kodu çalıştırmak için şu satırı ekleyebilirsiniz:
# await grup_uye_ekle("grup_id", 5, [1, 5])
