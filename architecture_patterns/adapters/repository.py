import abc

from architecture_patterns.domain.model import Batch
from sqlalchemy.orm.session import Session


class AbstractRepository(abc.ABC):
    @abc.abstractmethod
    def add(self, batch: Batch):
        ...

    @abc.abstractmethod
    def get(self, reference: str) -> Batch:
        ...

    @abc.abstractmethod
    def list(self) -> list[Batch]:
        ...


class SqlAlchemyRepository(AbstractRepository):
    def __init__(self, session: Session):
        self.session = session

    def add(self, batch: Batch):
        self.session.add(batch)
        self.session.commit()

    def get(self, reference: str) -> Batch:
        return self.session.query(Batch).filter_by(reference=reference).one()

    def list(self) -> list[Batch]:
        return self.session.query(Batch).all()
