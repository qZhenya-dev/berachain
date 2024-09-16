from contracts.BeraStake import BeraStake
from contracts.BeraMultiSwap import BeraMultiSwap
from contracts.BeraAddLiquidity import BeraAddLiquidity

from contracts.faucet import Faucet
from models.coins import Coins

from config import capsolver_token, delay_actions
from utils.file_manager import append_to_txt
from utils.logs import logger

from decimal import Decimal
import time, random


class Client:
    def __init__(self, account):
        self.coins = Coins()
        self.account = account

        logger.info(f"{self.account.private_key[:5]}..{self.account.private_key[-5:]} запуск бота..")

        self.bera_swap = BeraMultiSwap(self.account)
        self.bera_liquidity = BeraAddLiquidity(self.account)
        self.bera_stake = BeraStake(self.account)

        self.faucet = Faucet(
            token=capsolver_token,
            address=self.bera_swap.address,
            proxy=self.account.proxy
        )

        self.address = self.bera_swap.address
        self.acc_name = self.bera_swap.acc_name
        self.infinity = 57896044618658097711785492504343953926634992332820282019728792003956564819967

    def sleep(self, delay):
        s = random.randint(*delay)
        logger.info(f"{self.acc_name} ожидаем {s} сек..")
        time.sleep(s)

    def exchange_bera_to_coins(self, balance_bera, price_bera, price_coin1, price_coin2, balance_coin1, balance_coin2):
        total_usd_from_bera = balance_bera * price_bera

        coin1_usd_value = balance_coin1 * price_coin1
        coin2_usd_value = balance_coin2 * price_coin2

        total_usd = coin1_usd_value + coin2_usd_value + total_usd_from_bera

        target_each_usd_value = total_usd / 2

        coin1_needed_usd = target_each_usd_value - coin1_usd_value
        coin2_needed_usd = target_each_usd_value - coin2_usd_value

        coin1_needed = max(coin1_needed_usd / price_coin1, 0)
        coin2_needed = max(coin2_needed_usd / price_coin2, 0)

        coin1_needed = coin1_needed * price_coin1
        coin2_needed = coin2_needed * price_coin2

        return round(Decimal(coin1_needed / price_bera), 6), round(Decimal(coin2_needed / price_bera), 6)

    def swap_tokens(self):
        price_bera = self.bera_swap.get_price(self.coins.BERA.address, True)
        balance_bera = self.bera_swap.balance()
        coin1_needed = 0
        coin2_needed = 0

        if balance_bera >= 0.4:
            balance_bera *= Decimal(0.95)

            price_coin1 = self.bera_swap.get_price(self.coins.HONEY.address, True)
            balance_coin1 = self.bera_swap.token_balance(self.coins.HONEY.address)

            price_coin2 = self.bera_swap.get_price(self.coins.WBERA.address, True)
            balance_coin2 = self.bera_swap.token_balance(self.coins.WBERA.address)

            coin1_needed, coin2_needed = self.exchange_bera_to_coins(
                price_bera=price_bera,
                balance_bera=balance_bera,
                price_coin1=price_coin1,
                balance_coin1=balance_coin1,
                price_coin2=price_coin2,
                balance_coin2=balance_coin2
            )

            if coin1_needed > 0:
                self.bera_swap.swap_bera(self.coins.HONEY.address, coin1_needed)
                self.sleep(delay_actions)

            if coin2_needed > 0:
                self.bera_swap.wrap_bera(coin2_needed)
                self.sleep(delay_actions)
        else:
            logger.warning(f'{self.acc_name} недостаточно BERA на счёте для обмена')

        return balance_bera, coin1_needed, coin2_needed

    def add_liq(self, coin1_needed, coin2_needed):
        amount_add_liquidity = round(self.bera_liquidity.token_balance(self.coins.HONEY.address) * Decimal(0.99), 6)

        if amount_add_liquidity >= 0.01:
            coin1_allowance = self.bera_swap.get_allowance(self.coins.HONEY.address, "0xAB827b1Cc3535A9e549EE387A6E9C3F02F481B49")
            coin2_allowance = self.bera_swap.get_allowance(self.coins.WBERA.address, "0xAB827b1Cc3535A9e549EE387A6E9C3F02F481B49")

            if coin1_allowance < coin1_needed:
                self.bera_liquidity.approve(
                    contract=self.coins.HONEY,
                    spender="0xAB827b1Cc3535A9e549EE387A6E9C3F02F481B49",
                    amount=self.infinity,
                    address_to=self.coins.HONEY.address,
                )

            if coin2_allowance < coin2_needed:
                self.bera_liquidity.approve(
                    contract=self.coins.HONEY,
                    spender="0xAB827b1Cc3535A9e549EE387A6E9C3F02F481B49",
                    amount=self.infinity,
                    address_to=self.coins.WBERA.address,
                )

            if round(amount_add_liquidity) > 0:
                logger.info(f"{self.acc_name} добавление в пулл {amount_add_liquidity} HONEY..")
                self.bera_liquidity.add_liquidity("0xd28d852cbcc68dcec922f6d5c7a8185dbaa104b7", coin1=self.coins.HONEY, coin2=self.coins.WBERA, amount=amount_add_liquidity)
                self.sleep(delay_actions)
        else:
            logger.warning(f'{self.acc_name} недостаточно HONEY на счёте для добавления в пулл')

    def stake(self):
        amount_lp = self.bera_stake.token_balance(self.coins.HONEY_WBERA_LP.address)

        if amount_lp >= 0.01:
            lp_allowance = self.bera_swap.get_allowance(self.coins.HONEY_WBERA_LP.address, "0xAD57d7d39a487C04a44D3522b910421888Fb9C6d")
            if lp_allowance < amount_lp:
                self.bera_stake.approve(
                    contract=self.coins.HONEY,
                    spender="0xAD57d7d39a487C04a44D3522b910421888Fb9C6d",
                    amount=self.infinity,
                    address_to=self.coins.HONEY_WBERA_LP.address,
                )

            if round(amount_lp) > 0:
                logger.info(f"{self.acc_name} будет застейкано {amount_lp} {self.coins.HONEY_WBERA_LP.coin}")
                self.bera_stake.stake(amount_lp)
                self.sleep(delay_actions)
        else:
            logger.warning(f'{self.acc_name} недостаточно {self.coins.HONEY_WBERA_LP.coin} на счёте для стейкинга')

    def start(self):
        if self.faucet.faucet():
            self.sleep(delay_actions)

        balance_bera, coin1_needed, coin2_needed = self.swap_tokens()
        if balance_bera > 0:
            self.add_liq(coin1_needed, coin2_needed)
            self.stake()
            self.bera_stake.get_rewards()

            logger.info(f"{self.acc_name} на счёте {round(self.bera_stake.token_balance(self.coins.BGT.address), 6)} BGT")
        else:
            logger.warning(f"{self.acc_name} следующие шаги будут пропущены т.к. на балансе 0 bera")
