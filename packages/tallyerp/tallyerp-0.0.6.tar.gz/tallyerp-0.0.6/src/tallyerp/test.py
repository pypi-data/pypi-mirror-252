from dataclasses import dataclass, field
from typing import Optional, List


@dataclass
class Ledger:
    name: str
    parent: str
    openingBalance: float
    _id: Optional[str] = field(
        default=None,
        metadata=dict(
            name="name",
            type="Attribute",
        ),
    )

    def __post_init__(self):
        self._id = self.name


@dataclass
class TallyMessage:
    ledger: List[Ledger]


@dataclass
class Data:
    tallyMessage: TallyMessage


@dataclass
class StaticVariables:
    importDups: str = "@@DUPCOMBINE"


@dataclass
class Desc:
    StaticVariables: StaticVariables


@dataclass
class Body:
    desc: Desc
    data: Data


@dataclass
class Header:
    version: int = 1
    tallyRequest: str = "Import"
    type: str = "Data"
    id: str = "All Masters"


@dataclass
class Envelope:
    header: Header
    body: Body

ledger = Ledger(
    name="John",
    parent="Sundry Debtors",
    openingBalance=1000,
)

ledger2 = Ledger(
    name="John2",
    parent="Sundry Debtors",
    openingBalance=1000,
)

tallyMessage = TallyMessage(ledger=[])
data = Data(tallyMessage=tallyMessage)
desc = Desc(StaticVariables=StaticVariables())
body = Body(desc=desc, data=data)
header = Header()
envelope = Envelope(header=header, body=body)
from xsdata.formats.dataclass.serializers import XmlSerializer

serializer = XmlSerializer()
data = serializer.render(envelope)
print(data)
