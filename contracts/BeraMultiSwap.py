from contracts.default import Default
from utils.get_abi import get_abi

from decimal import Decimal


class BeraMultiSwap(Default):
    def __init__(self, account):
        super().__init__(account.private_key, "https://bartio.rpc.berachain.com/", get_abi("BeraMultiSwap"), "0x21e2C0AFd058A89FCf7caf3aEA3cB84Ae977B73D", account.proxy)

    def get_price(self, address, usdValue=False):
        resp = self.session.post(
            url="https://api.goldsky.com/api/public/project_clq1h5ct0g4a201x18tfte5iv/subgraphs/bgt-subgraph/v1000000/gn",
            json={
                "operationName": "GetTokenInformation",
                "variables": {"id": address.lower()},
                "query": "query GetTokenInformation($id: String) {\n  tokenInformation(id: $id) {\n    id\n    address\n    symbol\n    name\n    decimals\n    usdValue\n    beraValue\n    __typename\n  }\n}"
            })

        return Decimal(resp.json()["data"]["tokenInformation"]["beraValue"]) if not usdValue else Decimal(resp.json()["data"]["tokenInformation"]["usdValue"])

    def swap_bera(self, address, amount):
        price = self.get_price(address)

        data = self.contract.encode_abi("multiSwap", args=(
            [(36000, address, "0x0000000000000000000000000000000000000000", False)],
            int(self.gwei_to_wei(amount)),
            int(self.gwei_to_wei(amount/price*Decimal(0.99)))
        ))

        tx = {
            "chainId": self.w3.eth.chain_id,
            "data": data,
            "from": self.address,
            "nonce": self.nonce(),
            "to": "0x21e2C0AFd058A89FCf7caf3aEA3cB84Ae977B73D",
            "value": hex(self.gwei_to_wei(amount))
        }

        return self.send_transaction(tx, "swap")

    def wrap_bera(self, amount):
        tx = {
            "chainId": self.w3.eth.chain_id,
            "data": "0xd0e30db0",
            "from": self.address,
            "nonce": self.nonce(),
            "to": "0x7507c1dc16935B82698e4C63f2746A2fCf994dF8",
            "value": hex(self.gwei_to_wei(amount))
        }

        return self.send_transaction(tx, "wrap")
