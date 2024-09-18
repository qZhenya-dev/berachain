from art import text2art
from rich.console import Console

def first_message():
    console = Console()
    console.print(text2art("NEXT SOFTS\nBERACHAIN", font="tarty1"), style="rgb(235,160,63)")
    print()
    console.print("Телеграм с обновлениями и другими софтами:", style="rgb(86,171,227)", end=" ")
    console.print("https://t.me/next_softs\n", style="rgb(86,171,227)")
    print("-"*50+"\n")
