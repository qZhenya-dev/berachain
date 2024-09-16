import requests
from fake_useragent import UserAgent


def headers():
    return {
        "User-Agent": UserAgent(os='windows').random
    }

def create_session(proxy):
    session = requests.Session()
    if proxy:
        proxies = {
            'http': f"http://{proxy}",
            'https': f"http://{proxy}",
        }
        session.proxies = proxies

    session.headers = headers()

    return session

