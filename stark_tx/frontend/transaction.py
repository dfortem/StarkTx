from flask import Blueprint, render_template

from stark_tx.engine.decoders.transaction import decode_transaction
from stark_tx.engine.providers.sequencer import get_transaction, get_block
from stark_tx.frontend import frontend_route
from stark_tx.frontend.output import print_transaction

bp = Blueprint("transaction", __name__)


@frontend_route(bp, "/<int:tx_id>")
def route_transaction(tx_id):
    tx = starktx_transaction(tx_id)
    return render_template("transaction.html", transaction=tx), 200


def starktx_transaction(transaction_id: int) -> dict:
    raw_transaction = get_transaction(transaction_id)
    raw_block = (
        get_block(raw_transaction["block_id"])
        if "block_id" in raw_transaction
        else None
    )
    decoded_transaction = decode_transaction(raw_block, raw_transaction)
    print_transaction(decoded_transaction)

    return decoded_transaction
