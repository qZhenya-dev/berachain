from art import text2art
from colorama import Fore, init
from rich.console import Console

init()
def first_message():
    console = Console()
    print(Fore.CYAN, text2art("NEXT SOFTS\nBERACHAIN", font="doom"))
    console.print("Телеграм с обновлениями и другими софтами:", style="rgb(60,79,201)", end=" ")
    console.print("[underline]https://t.me/next_softs[/underline]\n", style="rgb(104,222,75)")
    print("-"*50+"\n")