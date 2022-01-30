from architecture_patterns.adapters.repository import AbstractRepository
from architecture_patterns.domain.model import Batch
from architecture_patterns.service_layer.unit_of_work import AbstractUnitOfWork


class FakeRepository(AbstractRepository):
    def __init__(self, batches: list[Batch]):
        self.batches = batches

    def add(self, batch: Batch):
        self.batches.append(batch)

    def get(self, reference: str) -> Batch:
        return next(batch for batch in self.batches if batch.reference == reference)

    def list(self) -> list[Batch]:
        return self.batches


class FakeUnitOfWork(AbstractUnitOfWork):
    def __init__(self):
        self.batches = FakeRepository([])
        self.committed = False

    def commit(self):
        self.committed = True

    def rollback(self):
        pass
