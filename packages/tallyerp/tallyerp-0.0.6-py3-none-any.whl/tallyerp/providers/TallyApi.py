import requests
import os
from tallyerp.config import TallyRequestTemplate, TALLY_URL_ENV_KEY


class TallyAPIProvider:
    def __init__(self):
        self.url = os.environ[TALLY_URL_ENV_KEY]
        self.headers = {
            "Content-Type": "text/xml, UTF-8, UTF-16, ASCII",
            'Content-Type': 'application/xml'
        }
        self.url = "http://192.168.0.11:9000"

    def post(self, request: str):
        res = requests.request("POST", self.url, data=request.encode('utf-8'), headers=self.headers)
        print(res.text)
        if res.status_code != 200:
            raise Exception("Error while calling API")
