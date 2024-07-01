import asyncio
import re
from telethon import TelegramClient, errors
from lib.session_kontrol import check_user_sessions
from lib.uyecekici2 import get_this_group_members
from json import dumps
from rich.console import Console
from colorama import init, Fore

with open("lib/config/zhedef.txt", "r+", encoding="utf-8") as dosya:
    HedefGruplar = [grup.replace("\n", "").strip() for grup in dosya.readlines()]


lg = Fore.LIGHTGREEN_EX
w = Fore.WHITE
cy = Fore.CYAN
ye = Fore.YELLOW
k = Fore.RED
n = Fore.RESET
colors = [lg, k, w, cy, ye]

async def grup_uyelerini_al(oturum, grup, filtre):

    client: TelegramClient = oturum['client']
    await client.connect()

    try:
        uyeler = await get_this_group_members(oturum, grup, filtre)
        return {'grup': grup, 'uyeler': uyeler or []}
    except errors.FloodWaitError as e:
        return {'grup': grup, 'hata': k+f'Flood Wait Error: {e.seconds} saniye bekleyin'}
    except errors.RPCError as e:
        return {'grup': grup, 'hata': k+f'RPC Error: {e}'}
    except Exception as e:
        return {'grup': grup, 'hata': k+f'Genel Hata: {str(e)}'}

async def grup_uyelerini_disa_aktar(filtre=None):
    console = Console()

    oturumlar = await check_user_sessions()

    console.print(cy+f"Yazılımda {len(oturumlar)} {cy} adet Hesap Var !\n", justify="center", width=70)

    uyeler = []

    async def grup_isle(oturum, grup):
        result = await grup_uyelerini_al(oturum, grup, filtre)
        if isinstance(result, Exception):
            console.print(k+f'HATA: {result}', justify='center', width=70)
        elif result:
            uyeler.extend(result['uyeler'])

    await asyncio.gather(*(grup_isle(oturum, grup) for oturum in oturumlar for grup in HedefGruplar))

    benzersiz_uyeler = [dict(girdi) for girdi in {tuple(ic_dict.items()) for ic_dict in uyeler}]
    sirali_uyeler = sorted(benzersiz_uyeler, key=lambda girdi: girdi.get('id', 0), reverse=True)
    json_verisi = dumps(sirali_uyeler, ensure_ascii=False, sort_keys=False, indent=2)

    with open('lib/config/uyeler.json', 'w+', encoding='utf-8') as kullanici_dosyasi:
        kullanici_dosyasi.write(json_verisi)

    console.print(lg+f'Toplam {len(benzersiz_uyeler)} {lg} Kullanıcı Çekildi.', justify='center', width=70)

if __name__ == "__main__":
    asyncio.run(grup_uyelerini_disa_aktar(filtre=re.compile(r'your_regex_pattern')))
