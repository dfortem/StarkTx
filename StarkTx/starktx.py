from flask import Flask, render_template

from StarkTx.providers.sequencer import get_block, get_transaction
from StarkTx.providers.semantics import load_semantics
from StarkTx.decoders.transaction import decode_transaction
from StarkTx.templates.output import print_transaction


def starktx_transaction(transaction_id: int) -> dict:
    raw_transaction = get_transaction(transaction_id)
    raw_block = get_block(raw_transaction['block_id']) if 'block_id' in raw_transaction else None
    decoded_transaction = decode_transaction(raw_block, raw_transaction)
    print_transaction(decoded_transaction)

    return decoded_transaction


app = Flask(__name__)
load_semantics()


@app.route("/")
def route_home():
    return "<p>StarkNet transaction decoder...</p>"


@app.route("/<int:tx_id>")
def route_transaction(tx_id):
    tx = starktx_transaction(tx_id)
    return render_template("transaction.html", transaction=tx), 200


app.run()
