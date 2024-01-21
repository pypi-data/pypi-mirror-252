from tallyerp.entities.tally import *
from xsdata.formats.dataclass.serializers import XmlSerializer


class TallyRequestProvider:
    def __init__(self):
        ...

    def getRequest(self, reqType: str, isMaster: bool, ledgers: List[Ledger]):
        tallyMessage = TallyMessage()
        for ledger in ledgers:
            tallyMessage.ledger.append(ledger)
        data = Data(tallyMessage=tallyMessage)
        desc = Desc(StaticVariables=StaticVariables())
        body = Body(desc=desc, data=data)
        header = Header()
        header.type = reqType
        if isMaster:
            header.id = "All Masters"
        envelope = Envelope(header=header, body=body)
        serializer = XmlSerializer()
        data = serializer.render(envelope)
        return data
