import requests

from contracts.default import Default
from utils.get_abi import get_abi
from utils.encode import get_data_byte64

from decimal import Decimal


class BeraAddLiquidity(Default):
    def __init__(self, account):
        super().__init__(account.private_key, "https://bartio.rpc.berachain.com/", get_abi("CrocSwapDex"), "0xAB827b1Cc3535A9e549EE387A6E9C3F02F481B49", account.proxy)
        self.croc_query_contract = Default(account.private_key, "https://bartio.rpc.berachain.com/", get_abi("CrocQuery"), "0x8685CE9Db06D40CBa73e3d09e6868FE476B5dC89", account.proxy)

    def get_price(self, address):
        resp = self.session.post(
            url="https://api.goldsky.com/api/public/project_clq1h5ct0g4a201x18tfte5iv/subgraphs/bgt-subgraph/v1000000/gn",
            json={
                "operationName": "GetTokenInformation",
                "variables": {"id": address.lower()},
                "query": "query GetTokenInformation($id: String) {\n  tokenInformation(id: $id) {\n    id\n    address\n    symbol\n    name\n    decimals\n    usdValue\n    beraValue\n    __typename\n  }\n}"
            })

        return Decimal(resp.json()["data"]["tokenInformation"]["beraValue"])

    def get_price_pool(self, coin1, coin2):
        resp = self.croc_query_contract.contract.functions.queryPrice(
            coin1.address,
            coin2.address,
            36000
        ).call()
        return resp

    def add_liquidity(self, lp_address, coin1, coin2, amount):
        price = self.get_price(coin1.address)
        price_pool = self.get_price_pool(coin1, coin2)

        data = get_data_byte64("0xa15112f9", hex(128), hex(64), hex(352), hex(32),
                               coin1.address.lower(), coin2.address.lower(), hex(36000),
                               0, 0, hex(self.gwei_to_wei(amount*price)), hex(int(price_pool*0.9995)),
                               hex(int(price_pool * 1.0005)), 0, lp_address.lower())

        tx = {
            "chainId": self.w3.eth.chain_id,
            "data": data,
            "from": self.address,
            "nonce": self.nonce(),
            "to": "0xAB827b1Cc3535A9e549EE387A6E9C3F02F481B49",
            "value": "0x0"
        }

        return self.send_transaction(tx, "add liquidity")
