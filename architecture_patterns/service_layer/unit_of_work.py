import abc

from architecture_patterns.adapters import repository
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# TODO: move this to config module
POSTGRES_URL = ""
DEFAULT_SESSION_FACTORY = sessionmaker(bind=create_engine(POSTGRES_URL))


class AbstractUnitOfWork(abc.ABC):
    products: repository.AbstractProductRepository

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.rollback()

    @abc.abstractmethod
    def commit(self):
        ...

    @abc.abstractmethod
    def rollback(self):
        ...


class SqlAlchemyUnitOfWork(AbstractUnitOfWork):
    def __init__(self, session_factory=DEFAULT_SESSION_FACTORY):
        self.session_factory = session_factory

    def __enter__(self):
        self.session = self.session_factory()
        self.products = repository.SqlAlchemyProductRepository(self.session)
        return super().__enter__()

    def __exit__(self, exc_type, exc_val, exc_tb):
        super().__exit__(exc_type, exc_val, exc_tb)
        self.session.close()
        # or it could be done like, so we commit if no exception
        # raised and rollback otherwise
        # if exc_type is None:
        #     self.commit()
        # else:
        #     self.rollback()

    def commit(self):
        self.session.commit()

    def rollback(self):
        self.session.rollback()
