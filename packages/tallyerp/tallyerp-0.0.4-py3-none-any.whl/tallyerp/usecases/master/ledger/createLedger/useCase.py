from .dto import CreateLedgerRequest, CreateLedgerResponse
from tallyerp.repositories.masters.Ledger import LedgerRepository


class CreateLedgerUseCase:
    def __init__(self, req: CreateLedgerRequest):
        self.request = req
        self.repo = LedgerRepository()

    def execute(self) -> CreateLedgerResponse:
        ledger = self.repo.create(self.request.ledger)
        return CreateLedgerResponse(ledger)
