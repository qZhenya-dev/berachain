import requests, time
from utils.logs import logger
from utils.session import create_session

class Faucet:
    def __init__(self, token, address, proxy=None):
        self.token = token
        self.address = address
        self.taskId = ""
        self.captcha = ""

        self.acc_name = f"{self.address[:5]}..{self.address[-5:]}"
        self.session = create_session(proxy)

    def create_task(self):
        resp = self.session.post("https://api.capsolver.com/createTask", json={
            "clientKey": self.token,
                "task": {
                    "type": "AntiTurnstileTaskProxyLess",
                    "websiteURL": "https://bartio.faucet.berachain.com/",
                    "websiteKey": "0x4AAAAAAARdAuciFArKhVwt",
                }
        })

        self.taskId = resp.json()["taskId"]
        logger.info(f"{self.acc_name} решаем капчу {self.taskId}..")

    def task_status(self):
        for i in range(15):
            try:
                time.sleep(5)

                resp = self.session.post("https://api.capsolver.com/getTaskResult", json={
                    "clientKey": self.taskId,
                    "taskId": self.taskId
                }).json()

                if resp["status"] == "ready":
                    logger.info(f"{self.acc_name} капча решена")
                    self.captcha = resp["solution"]["token"]
                    return True
            except Exception as e:
                logger.error(f"{self.acc_name} {self.taskId} {e}")

        return False

    def get_token(self):
        self.session.headers["Authorization"] = f"Bearer {self.captcha}"
        resp = self.session.post(f"https://bartio-faucet.berachain-devnet.com/api/claim?address={self.address}", json={"address": self.address})

        status_code = resp.status_code
        if status_code == 200:
            logger.success(f"{self.acc_name} получили токены BERA")
            return True

        elif status_code == 429:
            logger.info(f"{self.acc_name} получение токенов на перезарядке")
        elif status_code == 402:
            logger.info(f"{self.acc_name} на балансе менее 0.001 ETH")

        return False

    def faucet(self):
        while True:
            self.create_task()
            if self.task_status():
                break

        return self.get_token()
