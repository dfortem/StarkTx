from datetime import datetime

from app.engine.decoders.trace import decode_trace


def decode_transaction(chain_id: str, block: dict, transaction: dict, traces: dict) -> dict:

    decoded_transaction = dict()
    decoded_transaction["chain_id"] = chain_id or 'mainnet'
    decoded_transaction["block_number"] = transaction["block_number"] if "block_number" in transaction else None
    decoded_transaction["block_hash"] = transaction["block_hash"] if "block_hash" in transaction else None

    decoded_transaction["timestamp"] = (
        datetime.fromtimestamp(block["timestamp"])
        if block and "timestamp" in block
        else None
    )

    decoded_transaction["transaction_hash"] = transaction["transaction"]["transaction_hash"]
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
        if block and block != 'pending'
        else None
    )

    decoded_transaction["transaction_index"] = receipt["transaction_index"] if receipt else None
    decoded_transaction['l2_to_l1_messages'] = receipt['l2_to_l1_messages'] if receipt else []

    decoded_transaction['calls'], decoded_transaction['events'] = \
        decode_trace(chain_id, transaction["block_hash"], traces["function_invocation"], None, 0)

    if decoded_transaction['events']:
        decoded_transaction['events'].sort(key=lambda x: x['order'])

    decoded_transaction['execution_resources'] = receipt['execution_resources'] if receipt else []

    return decoded_transaction
