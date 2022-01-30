from flask import Flask, request
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from architecture_patterns import orm
from architecture_patterns import repository
from architecture_patterns import model

# TODO: move this to configuration module
POSTGRES_URL = ""

orm.start_mappers()
get_session = sessionmaker(bind=create_engine(POSTGRES_URL))
app = Flask(__name__)


# TODO: validation of incoming data
@app.route("/allocate", methods=["POST"])
def allocate():
    data = request.json()
    line = model.OrderLine(
        order_id=data["order_id"],
        sku=data["sku"],
        quantity=data["quantity"]
    )

    session = get_session()
    batches = repository.SqlAlchemyRepository(session).list()
    batch_reference = model.allocate(line, batches)

    return {"batch_reference": batch_reference}, 201
