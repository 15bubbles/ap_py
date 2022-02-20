from dataclasses import dataclass
from typing import Any, Optional

import datetime


@dataclass(frozen=True)
class OrderLine:
    order_id: str
    sku: str
    quantity: int


class Batch:
    def __init__(
        self, reference: str, sku: str, quantity: int, eta: Optional[datetime.date]
    ):
        self.reference = reference
        self.sku = sku
        self.eta = eta
        self._quantity = quantity
        self._allocations = set()  # type: set[OrderLine]

    def __eq__(self, other: Any) -> bool:
        if not isinstance(other, Batch):
            return False

        return self.reference == other.reference

    def __hash__(self):
        return hash(self.reference)

    @property
    def allocated_quantity(self) -> int:
        return sum(line.quantity for line in self._allocations)

    @property
    def available_quantity(self) -> int:
        return self._quantity - self.allocated_quantity

    def allocate(self, line: OrderLine) -> None:
        if self.can_allocate(line):
            self._allocations.add(line)

    def deallocate(self, line: OrderLine) -> None:
        if line in self._allocations:
            self._allocations.remove(line)

    def can_allocate(self, line: OrderLine) -> bool:
        return self.sku == line.sku


class OutOfStock(Exception):
    ...


def allocate(line: OrderLine, batches: list[Batch]) -> str:
    try:
        batch = next(batch for batch in batches if batch.can_allocate(line))
    except StopIteration:
        raise OutOfStock(f"Out of stock for sku {line.sku}")

    batch.allocate(line)
    return batch.reference


class Product:
    def __init__(self, sku: str, batches: list[Batch], version_number: int = 0):
        self.sku = sku
        self.batches = batches
        self.version_number = version_number

    def allocate(self, line: OrderLine) -> str:
        try:
            batch = next(batch for batch in self.batches if batch.can_allocate(line))
        except StopIteration:
            raise OutOfStock(f"Out of stock for sku {line.sku}")

        batch.allocate(line)
        self.version_number += 1
        return batch.reference
