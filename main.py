from contracts.BeraStake import BeraStake
from contracts.BeraMultiSwap import BeraMultiSwap
from contracts.BeraAddLiquidity import BeraAddLiquidity

from models.accounts import Accounts
from contracts.faucet import Faucet
from models.coins import Coins

from utils.first_message import first_message
from core.client import Client
from utils.logs import logger
from config import *

import threading, time, random


def start_farming(accounts):
    clients = [Client(account) for account in accounts]
    timeouts = {}

    while True:
        try:
            time.sleep(10)
            random.shuffle(clients)
            for i, client in enumerate(clients):
                acc_name = client.acc_name

                if acc_name not in timeouts:
                    timeouts[acc_name] = int(time.time() + random.randint(*delay_start) * (i+1))

                if time.time() >= timeouts[acc_name]:
                    logger.info(f"{acc_name} запуск..")
                    threading.Thread(target=client.start).start()
                    timeouts[acc_name] = int(time.time() + random.randint(*delay_staking) * (i+1))

        except Exception as e:
            logger.error(e)

def check_balances_bgt(accounts):
    def check_balance(account):
        bera = BeraStake(account)
        logger.info(f"{bera.acc_name} - {round(bera.token_balance(coins.BGT.address), 6)} {coins.BGT.coin}")

    coins = Coins()
    for account in accounts:
        threading.Thread(target=check_balance, args=(account,)).start()

def main():
    accounts_manager = Accounts()
    accounts_manager.loads_accs()
    accounts = accounts_manager.accounts

    action = input("> 1. Запустить фарминг\n"
                   "> 2. Посмотреть балансы BGT\n"
                   "> ")
    print("-"*50+"\n")

    if action == "1":
        start_farming(accounts)
    elif action == "2":
        check_balances_bgt(accounts)
    else:
        logger.warning(f"Выбран вариант, которого нет!")

if __name__ == '__main__':
    first_message()
    main()


