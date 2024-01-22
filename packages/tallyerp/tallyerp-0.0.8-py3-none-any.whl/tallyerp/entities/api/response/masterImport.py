from dataclasses import dataclass, field
from typing import Optional, List
from tallyerp.entities import Ledger
from tallyerp.entities.masters.group import Group
from .common import *


@dataclass
class ImportResult:
    CREATED: int
    ALTERED: int
    DELETED: int


@dataclass
class Data:
    IMPORTRESULT: ImportResult


@dataclass
class Desc:
    CMPINFO: CompInfo
    CMPINFOEX: CmpInfoEx


@dataclass
class Body:
    DESC: Desc
    DATA: Data


@dataclass
class Header:
    VERSION: int
    STATUS: str


@dataclass
class Envelope:
    HEADER: Header
    BODY: Body
