from .dto import CreateLedgerRequest, CreateLedgerResponse
from tallyerp.repositories.masters.Ledger import LedgerRepository


class CreateLedgerUseCase:
    def __init__(self, req: CreateLedgerRequest):
        self.request = req
        self.repo = LedgerRepository()

    def execute(self) -> CreateLedgerResponse:
        res = self.repo.create(self.request.ledger)
        return CreateLedgerResponse(
            created=res.response.BODY.DATA.IMPORTRESULT.CREATED,
            altered=res.response.BODY.DATA.IMPORTRESULT.ALTERED,
            deleted=res.response.BODY.DATA.IMPORTRESULT.DELETED,
        )
