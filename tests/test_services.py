from architecture_patterns.model import Batch
from architecture_patterns.repository import AbstractRepository


class FakeRepository(AbstractRepository):
    def __init__(self, batches: list[Batch]):
        self.batches = batches

    def add(self, batch: Batch):
        self.batches.append(batch)

    def get(self, reference: str) -> Batch:
        return next(batch for batch in self.batches if batch.reference == reference)

    def list(self) -> list[Batch]:
        return self.batches
