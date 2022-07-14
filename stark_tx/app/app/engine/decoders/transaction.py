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

from datetime import datetime

from app.engine.decoders.trace import decode_trace


def decode_transaction(
    chain_id: str, block: dict, transaction: dict, traces: dict
) -> dict:

    decoded_transaction = dict()
    decoded_transaction["chain_id"] = chain_id or "mainnet"
    decoded_transaction["block_number"] = (
        transaction["block_number"] if "block_number" in transaction else None
    )
    decoded_transaction["block_hash"] = (
        transaction["block_hash"] if "block_hash" in transaction else None
    )

    decoded_transaction["timestamp"] = (
        datetime.fromtimestamp(block["timestamp"])
        if block and "timestamp" in block
        else None
    )

    decoded_transaction["transaction_hash"] = transaction["transaction"][
        "transaction_hash"
    ]
    decoded_transaction["signature"] = transaction["transaction"].get("signature", [])

    decoded_transaction["type"] = transaction["transaction"]["type"]
    decoded_transaction["status"] = transaction["status"]

    decoded_transaction["error"] = (
        transaction["transaction_failure_reason"]["error_message"]
        if "transaction_failure_reason" in transaction
        else None
    )

    receipt = (
        [
            receipt
            for receipt in block["transaction_receipts"]
            if receipt["transaction_hash"]
            == transaction["transaction"]["transaction_hash"]
        ][0]
        if block and block != "pending"
        else None
    )

    decoded_transaction["transaction_index"] = (
        receipt["transaction_index"] if receipt else None
    )
    decoded_transaction["l2_to_l1_messages"] = (
        receipt["l2_to_l1_messages"] if receipt else []
    )

    decoded_transaction["calls"], decoded_transaction["events"] = decode_trace(
        chain_id, transaction["block_hash"], traces["function_invocation"], None, 0
    )

    if decoded_transaction["events"]:
        decoded_transaction["events"].sort(key=lambda x: x["order"])

    decoded_transaction["execution_resources"] = (
        receipt["execution_resources"] if receipt else []
    )

    return decoded_transaction
