from web3 import Web3
from utils.get_abi import get_abi

class CoinInfo:
    def __init__(self, coin, address, abi):
        w3 = Web3()

        self.coin = coin
        self.address = w3.to_checksum_address(address)
        self.abi = abi

class Coins:
    BERA = CoinInfo(coin="BERA", address="0x7507c1dc16935B82698e4C63f2746A2fCf994dF8", abi=get_abi("bera"))
    WBERA = CoinInfo(coin="WBERA", address="0x7507c1dc16935B82698e4C63f2746A2fCf994dF8", abi=get_abi("bera"))
    HONEY = CoinInfo(coin="HONEY", address="0x0E4aaF1351de4c0264C5c7056Ef3777b41BD8e03", abi=get_abi("honey"))
    BGT = CoinInfo(coin="BGT", address="0xbDa130737BDd9618301681329bF2e46A016ff9Ad", abi=get_abi("bgt"))
    HONEY_WBERA_LP = CoinInfo(coin="HONEY-WBERA-LP", address="0xd28d852cbcc68DCEC922f6d5C7a8185dBaa104B7", abi=get_abi("HONEY-WBERA-LP"))
