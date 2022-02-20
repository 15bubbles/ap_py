import abc

from architecture_patterns.domain import model
from sqlalchemy.orm.session import Session


class AbstractRepository(abc.ABC):
    @abc.abstractmethod
    def add(self, batch: model.Batch):
        ...

    @abc.abstractmethod
    def get(self, reference: str) -> model.Batch:
        ...

    @abc.abstractmethod
    def list(self) -> list[model.Batch]:
        ...


class SqlAlchemyRepository(AbstractRepository):
    def __init__(self, session: Session):
        self.session = session

    def add(self, batch: model.Batch):
        self.session.add(batch)
        self.session.commit()

    def get(self, reference: str) -> model.Batch:
        return self.session.query(model.Batch).filter_by(reference=reference).one()

    def list(self) -> list[model.Batch]:
        return self.session.query(model.Batch).all()


class AbstractProductRepository(abc.ABC):
    @abc.abstractmethod
    def add(self, product: model.Product) -> None:
        ...

    @abc.abstractmethod
    def get(self, sku: str) -> model.Product:
        ...


class SqlAlchemyProductRepository(AbstractProductRepository):
    def __init__(self, session: Session):
        self.session = session

    def add(self, product: model.Product):
        self.session.add(product)
        self.session.commit()

    def get(self, sku: str) -> model.Product:
        return self.session.query(model.Product).filter_by(sku=sku).first()
