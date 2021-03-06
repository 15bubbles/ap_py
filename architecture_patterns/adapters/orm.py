from sqlalchemy.orm import mapper, relationship
from sqlalchemy import MetaData, Table, Column, Integer, String, ForeignKey, Date

from architecture_patterns.domain import model

metadata = MetaData()

order_lines = Table(
    "order_lines",
    metadata,
    Column("id", Integer, primary_key=True, autoincrement=True),
    Column("sku", String(255)),
    Column("quantity", Integer, nullable=False),
    Column("order_id", String(255)),
)

products = Table(
    "products",
    metadata,
    Column("sku", String(255), primary_key=True),
    Column("version_number", Integer, nullable=False, server_default=0),
)

batches = Table(
    "batches",
    metadata,
    Column("id", Integer, primary_key=True, autoincrement=True),
    Column("sku", ForeignKey("products.sku")),
    Column("reference", String(255)),
    Column("eta", Date, nullable=True),
)

allocations = Table(
    "allocations",
    metadata,
    Column("id", Integer, primary_key=True, autoincrement=True),
    Column("order_line_id", ForeignKey("order_lines.id")),
    Column("batch_id", ForeignKey("batches.id")),
)


def start_mappers():
    order_lines_mapper = mapper(model.OrderLine, order_lines)
    batches_mapper = mapper(
        model.Batch,
        batches,
        properties={
            "_allocations": relationship(
                order_lines_mapper,
                secondary=allocations,
                collection_class=set,
            )
        },
    )
    mapper(
        model.Product, products, properties={"batches": relationship(batches_mapper)}
    )
