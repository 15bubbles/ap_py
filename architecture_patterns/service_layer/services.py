from typing import Optional
import datetime
from collections.abc import Iterable

from architecture_patterns.domain import model
from architecture_patterns.service_layer.unit_of_work import AbstractUnitOfWork


class InvalidSku(Exception):
    ...


# this can be more efficient most probably
def is_valid_sku(sku: str, batches: Iterable[model.Batch]) -> bool:
    return sku in {batch.sku for batch in batches}


def add_batch(
    reference: str,
    sku: str,
    quantity: int,
    eta: Optional[datetime.date],
    uow: AbstractUnitOfWork,
) -> None:
    with uow:
        product = uow.products.get(sku=sku)

        if product is None:
            product = model.Product(sku, batches=[])
            uow.products.add(product)

        product.batches.append(model.Batch(reference, sku, quantity, eta))
        uow.commit()


def allocate(line: model.OrderLine, uow: AbstractUnitOfWork) -> str:
    with uow:
        product = uow.products.get(sku=line.sku)

        if product is None:
            raise InvalidSku(f"Invalid sku '{line.sku}'")

        batch_reference = product.allocate(line)
        uow.commit()

        return batch_reference
