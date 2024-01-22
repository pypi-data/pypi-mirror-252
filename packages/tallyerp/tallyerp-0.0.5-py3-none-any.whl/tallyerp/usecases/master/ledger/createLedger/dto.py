from dataclasses import dataclass

from tallyerp.entities.masters.ledger import Ledger


@dataclass
class CreateLedgerRequest:
    ledger: Ledger

@dataclass
class CreateLedgerResponse:
    ledger: Ledger
