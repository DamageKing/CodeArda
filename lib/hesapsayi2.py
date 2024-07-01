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

async def list_accounts_async(console, folder_path, account_type):
    accounts = list_accounts(folder_path)
    table = Table(title=f"[cyan]{account_type} Hesaplar[/cyan]")
    table.add_column("Hesaplar", style="cyan", header_style="bold")
    for account in accounts:
        table.add_row(f"[green]{account}[/green]")
    console.print(table)

async def trman():
    try:
        console = Console()
        tasks = [
            list_accounts_async(console, SESSIONS_PATH, "Sorunsuz"),
            list_accounts_async(console, BAN_PATH, "Banlı"),
            list_accounts_async(console, f"{SPAM_PATH}Until/", "Spam - Until"),
            list_accounts_async(console, f"{SPAM_PATH}Persist/", "Spam - Persist"),
        ]
        await asyncio.gather(*tasks)

    except Exception as e:
        print(f"{Fore.RED}Hata: {str(e)}")

if __name__ == "__main__":
    asyncio.run(trman())
