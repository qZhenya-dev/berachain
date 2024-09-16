from utils.file_manager import txt_to_list


class Account:
    def __init__(self, private_key, proxy):
        self.private_key = private_key
        self.proxy = proxy

class Accounts:
    def __init__(self):
        self.accounts = []

    def loads_accs(self):
        private_keys = txt_to_list("private_keys")
        proxies = txt_to_list("proxies")

        for i, private_key in enumerate(private_keys):
            self.accounts.append(Account(private_key=private_key, proxy=proxies[i]))
