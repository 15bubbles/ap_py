from collections.abc import Iterable

from sqlalchemy.orm import Session

from architecture_patterns import model
from architecture_patterns.repository import AbstractRepository


class InvalidSku(Exception):
    ...


# this can be more efficient most probably
def is_valid_sku(sku: str, batches: Iterable[model.Batch]) -> bool:
    return sku in {batch.sku for batch in batches}


def allocate(line: model.OrderLine, repository: AbstractRepository, session: Session) -> str:
    batches = repository.list()

    if not is_valid_sku(line.sku, batches):
        raise InvalidSku(f"Invalid sku '{line.sku}'")

    batch_reference = model.allocate(line, batches)
    session.commit()

    return batch_reference
