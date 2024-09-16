import requests

from contracts.default import Default
from utils.get_abi import get_abi
from utils.encode import get_data_byte64

from decimal import Decimal


class BeraStake(Default):
    def __init__(self, account):
        super().__init__(account.private_key, "https://bartio.rpc.berachain.com/", get_abi("bera1"), "0xd28d852cbcc68DCEC922f6d5C7a8185dBaa104B7", account.proxy)

    def stake(self, amount):
        data = get_data_byte64("0xa694fc3a", hex(self.gwei_to_wei(amount)))

        tx = {
            "chainId": self.w3.eth.chain_id,
            "data": data,
            "from": self.address,
            "nonce": self.nonce(),
            "to": "0xAD57d7d39a487C04a44D3522b910421888Fb9C6d",
            "value": "0x0"
        }

        return self.send_transaction(tx, "stake")

    def get_rewards(self):
        data = get_data_byte64("0xc00007b0", self.address)

        tx = {
            "chainId": self.w3.eth.chain_id,
            "data": data,
            "from": self.address,
            "nonce": self.nonce(),
            "to": "0xAD57d7d39a487C04a44D3522b910421888Fb9C6d",
            "value": "0x0"
        }

        return self.send_transaction(tx, "claim rewards")
