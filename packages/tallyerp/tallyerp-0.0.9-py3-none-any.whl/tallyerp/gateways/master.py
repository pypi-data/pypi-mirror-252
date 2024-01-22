from tallyerp.entities.masters.ledger import Ledger
from tallyerp.usecases import *


class MasterGateway:
    def __init__(self):
        ...

    def createLedger(self, ledgerName:str, parent: str, openingBalance: int) -> CreateLedgerResponse:
        dto =  CreateLedgerRequest(
            ledger = Ledger(
                name = ledgerName,
                parent = parent,
                openingBalance = openingBalance,
                action="Create"
            )
        )
        useCase = CreateLedgerUseCase(dto)
        return useCase.execute()