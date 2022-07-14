#  Copyright 2022 Token Flow Insights
#
#  Licensed under the Apache License, Version 2.0 (the "License");
#  you may not use this file except in compliance with the License.
#  You may obtain a copy of the License at: http://www.apache.org/licenses/LICENSE-2.0
#
#  Unless required by applicable law or agreed to in writing, software distributed under
#  the License is distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS
#  OF ANY KIND, either express or implied.
#
#  See the License for the specific language governing permissions and limitations
#  under the License.
#
#  The product contains trademarks and other branding elements of Token Flow Insights SA
#  which are not licensed under the Apache 2.0 license. When using or reproducing the code,
#  please remove the trademark and/or other branding elements.
#

from typing import Optional

from flask import Blueprint, render_template

from app.engine.decoders.transaction import decode_transaction
from app.engine.providers.sequencer import (
    get_transaction,
    get_block_hash,
    get_transaction_trace,
)
from app.frontend import frontend_route

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
        (
            get_block_hash(chain_id, raw_transaction["block_hash"])
            if "block_hash" in raw_transaction
            else None
        )
        if raw_transaction["block_hash"] != "pending"
        else "pending"
    )

    raw_traces = get_transaction_trace(chain_id, transaction_hash)

    if not raw_traces or not raw_traces["function_invocation"]["selector"]:
        raw_traces = dict(
            function_invocation=dict(
                type=raw_transaction["transaction"]["type"],
                caller_address=None,
                contract_address=raw_transaction["transaction"]["contract_address"],
                code_address=raw_transaction["transaction"]["contract_address"],
                selector=raw_transaction["transaction"].get(
                    "entry_point_selector", "constructor"
                ),
                entry_point_type=raw_transaction["transaction"].get(
                    "entry_point_type", "CONSTRUCTOR"
                ),
                calldata=raw_transaction["transaction"].get("calldata")
                or raw_transaction["transaction"].get("constructor_calldata")
                or [],
                result=raw_transaction["transaction"].get("result", []),
                internal_calls=[],
            )
        )

    decoded_transaction = decode_transaction(
        chain_id, raw_block, raw_transaction, raw_traces
    )

    return decoded_transaction
