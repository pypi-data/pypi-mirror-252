from tallyerp.entities.masters.ledger import Ledger
from tallyerp.usecases import *


class MasterGateway:
    def __init__(self):
        ...

    def createLedger(self, ledgerName:str, parent: str, openingBalance: int) -> Ledger:
        dto =  CreateLedgerRequest(
            ledger = Ledger(
                name = ledgerName,
                parent = parent,
                openingBalance = openingBalance
            )
        )
        useCase = CreateLedgerUseCase(dto)
        return useCase.execute()