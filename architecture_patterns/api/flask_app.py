from flask import Flask, request
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from architecture_patterns.adapters import orm, repository
from architecture_patterns.domain import model
from architecture_patterns.service_layer import services

# TODO: move this to configuration module
POSTGRES_URL = ""

orm.start_mappers()
get_session = sessionmaker(bind=create_engine(POSTGRES_URL))
app = Flask(__name__)


@app.route("/allocate", methods=["POST"])
def allocate():
    try:
        data = request.json()
        line = model.OrderLine(
            order_id=data["order_id"],
            sku=data["sku"],
            quantity=data["quantity"]
        )
    except KeyError:  # TODO: calling `json` might raise some error as well, include it
        return {"message": "Invalid data"}

    session = get_session()
    repo = repository.SqlAlchemyRepository(session)

    try:
        batch_reference = services.allocate(line, repo, session)
    except (model.OutOfStock, services.InvalidSku) as e:
        return {"message": str(e)}, 400

    return {"batch_reference": batch_reference}, 201
