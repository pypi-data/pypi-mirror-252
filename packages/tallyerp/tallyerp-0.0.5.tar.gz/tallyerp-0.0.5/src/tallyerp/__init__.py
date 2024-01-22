from tallyerp.gateways.tally import TallyGateway
from tallyerp.config import TALLY_URL
import os

def connect(tallyURL: str = TALLY_URL):
    if tallyURL:
        os.environ["TALLY_API_URL"] = tallyURL
        TALLY_URL =  tallyURL
    print(TALLY_URL)
    return TallyGateway()