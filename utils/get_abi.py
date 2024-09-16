import os
import json

def get_abi(name):
    try:
        with open(f"abis/{name}.json", "r") as f:
            data = f.read()
            f.close()
            if data:
                return json.loads(data)
    except FileNotFoundError:
        pass

    return []



