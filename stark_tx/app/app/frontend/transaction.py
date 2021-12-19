from flask import Blueprint, render_template

from app.engine.decoders.transaction import decode_transaction
from app.engine.providers.sequencer import get_transaction, get_block
from app.frontend import frontend_route
from app.frontend.output import print_transaction

bp = Blueprint("transactions", __name__)


@frontend_route(bp, "/<string:chain_id>/<string:tx_hash>/")
def route_transaction(chain_id: str, tx_hash: str):
    tx = starktx_transaction(tx_hash)
    return render_template("transaction.html", transaction=tx), 200


def starktx_transaction(transaction_hash: str) -> dict:
    raw_transaction = get_transaction(transaction_hash)
    raw_block = (
        get_block(raw_transaction["block_hash"])
        if "block_hash" in raw_transaction
        else None
    )
    decoded_transaction = decode_transaction(raw_block, raw_transaction)
    print_transaction(decoded_transaction)

    return decoded_transaction
