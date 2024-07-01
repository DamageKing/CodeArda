import os
import asyncio
from rich.console import Console
from rich.table import Table
from colorama import init, Fore

init(autoreset=True)

SESSIONS_PATH = "sessions/"
BAN_PATH = f"{SESSIONS_PATH}Banlanan/"
SPAM_PATH = f"{SESSIONS_PATH}Spam/"

def list_accounts(folder_path):
    accounts = []
    for file in os.listdir(folder_path):
        if file.endswith(".session"):
            accounts.append(file.replace('.session', ''))
    return accounts

def create_table(account_type, accounts):
    table = Table(title=f"[cyan]{account_type} Hesaplar[/cyan]")
    table.add_column("Numara", style="cyan", header_style="bold")
    table.add_column("Hesaplar", style="cyan", header_style="bold")
    for index, account in enumerate(accounts, start=1):
        table.add_row(f"[yellow]{index}[/yellow]", f"[green]{account}[/green]")
    return table

def list_and_choose(folder_path, account_type):
    accounts = list_accounts(folder_path)
    if not accounts:
        print(f"{account_type} Hesaplar bulunamadı.")
        return None

    console = Console()
    table = create_table(account_type, accounts)
    console.print(table)

    try:
        choice = int(input(f"\n{Fore.CYAN}Silmek istediğiniz hesabın numarasını girin (Çıkış için 0): "))
        if choice == 0:
            return None
        elif 1 <= choice <= len(accounts):
            return accounts[choice - 1]
        else:
            print(f"{Fore.RED}Geçersiz bir seçim yaptınız. Lütfen tekrar deneyin.")
            return None
    except ValueError:
        print(f"{Fore.RED}Geçersiz bir giriş yaptınız. Lütfen bir sayı girin.")
        return None

async def delete_account(account_path, account_type):
    try:
        os.remove(account_path)
        print(f"{Fore.LIGHTGREEN_EX}{account_type} Hesap başarıyla silindi.")
    except FileNotFoundError:
        print(f"{Fore.RED}{account_type} Hesap bulunamadı.")

async def delete_accounts_async():
    try:
        while True:
            console = Console()
            console.clear()
            
            print(f"{Fore.LIGHTMAGENTA_EX}1. Sorunsuz Hesaplar\n2. Banlı Hesaplar\n3. Spam - Until Hesaplar\n4. Spam - Persist Hesaplar\n0. Çıkış\n")

            choice = input(f"{Fore.CYAN}Hangi klasördeki hesapları silmek istediğinizi seçin (0-4): ")

            if choice == "0":
                break

            folder_path = None
            account_type = None

            if choice == "1":
                folder_path = SESSIONS_PATH
                account_type = "Sorunsuz"
            elif choice == "2":
                folder_path = BAN_PATH
                account_type = "Banlı"
            elif choice == "3":
                folder_path = f"{SPAM_PATH}Until/"
                account_type = "Spam - Until"
            elif choice == "4":
                folder_path = f"{SPAM_PATH}Persist/"
                account_type = "Spam - Persist"
            else:
                print(f"{Fore.RED}Geçersiz bir seçim yaptınız. Lütfen tekrar deneyin.")
                continue

            chosen_account = list_and_choose(folder_path, account_type)

            if chosen_account:
                account_path = f"{folder_path}{chosen_account}.session"
                await delete_account(account_path, account_type)

            await asyncio.sleep(1)  # Asenkron işlemi kontrol etmek için kısa bir bekleme ekledik

    except Exception as e:
        print(f"{Fore.RED}Hata: {str(e)}")

if __name__ == "__main__":
    asyncio.run(delete_accounts_async())
