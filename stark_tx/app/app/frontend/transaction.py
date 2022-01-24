from typing import Optional

from flask import Blueprint, render_template

from app.engine.decoders.transaction import decode_transaction
from app.engine.providers.sequencer import get_transaction, get_block_hash
from app.frontend import frontend_route
from app.frontend.output import print_transaction

bp = Blueprint("transactions", __name__)


@frontend_route(bp, "/<string:tx_hash>/")
@frontend_route(bp, "/<string:chain_id>/<string:tx_hash>/")
def route_transaction(
    tx_hash: str, chain_id: Optional[str] = None
) -> tuple["render_template", int]:
    tx = starktx_transaction(chain_id, tx_hash)
    return render_template("transaction.html", transaction=tx), 200


def starktx_transaction(chain_id: str, transaction_hash: str) -> dict:
    raw_transaction = get_transaction(chain_id, transaction_hash)
    raw_block = (
        get_block_hash(chain_id, raw_transaction["block_hash"])
        if "block_hash" in raw_transaction
        else None
    ) if raw_transaction["block_hash"] != 'pending' else 'pending'
    decoded_transaction = decode_transaction(chain_id, raw_block, raw_transaction)
    print_transaction(decoded_transaction)

    return decoded_transaction
