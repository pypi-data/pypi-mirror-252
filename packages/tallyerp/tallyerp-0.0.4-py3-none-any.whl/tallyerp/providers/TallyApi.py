import requests
from tallyerp.config import TallyRequestTemplate, TALLY_URL


class TallyAPIProvider:
    def __init__(self):
        self.url = TALLY_URL
        self.headers = {
            "Content-Type": "text/xml, UTF-8, UTF-16, ASCII",
            "Accept": "application/xml",
        }

    def post(self, request: str):
        res = requests.post(self.url, data=request, headers=self.headers)
        if res.status_code != 200:
            raise Exception("Error while calling API")
