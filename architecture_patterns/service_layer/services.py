from collections.abc import Iterable

from architecture_patterns.domain import model
from architecture_patterns.service_layer.unit_of_work import AbstractUnitOfWork


class InvalidSku(Exception):
    ...


# this can be more efficient most probably
def is_valid_sku(sku: str, batches: Iterable[model.Batch]) -> bool:
    return sku in {batch.sku for batch in batches}


def allocate(line: model.OrderLine, uow: AbstractUnitOfWork) -> str:
    with uow:
        batches = uow.batches.list()

        if not is_valid_sku(line.sku, batches):
            raise InvalidSku(f"Invalid sku '{line.sku}'")

        batch_reference = model.allocate(line, batches)
        uow.commit()

        return batch_reference
