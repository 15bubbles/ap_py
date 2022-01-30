from sqlalchemy.orm import mapper
from sqlalchemy import MetaData, Table, Column, Integer, String

from architecture_patterns.domain.model import OrderLine

metadata = MetaData()

order_lines = Table(
    "order_lines",
    metadata,
    Column("id", Integer, primary_key=True, autoincrement=True),
    Column("sku", String(255)),
    Column("quantity", Integer, nullable=False),
    Column("order_id", String(255)),
)


def start_mappers():
    mapper(OrderLine, order_lines)
