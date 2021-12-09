from datetime import datetime

from app.engine.decoders.parameter import decode_parameters
from app.engine.providers.semantics import get_semantics


def decode_transaction(block: dict, transaction: dict) -> dict:
    semantics = get_semantics(
        transaction["transaction"]["contract_address"], transaction["block_hash"]
    )
    decoded_transaction = dict()
    decoded_transaction["block_hash"] = (
        transaction["block_hash"] if "block_hash" in transaction else None
    )
    decoded_transaction["block_number"] = (
        transaction["block_number"] if "block_number" in transaction else None
    )
    decoded_transaction["timestamp"] = (
        datetime.fromtimestamp(block["timestamp"])
        if block and "timestamp" in block
        else None
    )

    decoded_transaction["transaction_hash"] = transaction["transaction"][
        "transaction_hash"
    ]
    decoded_transaction["type"] = transaction["transaction"]["type"]
    decoded_transaction["transaction_index"] = (
        transaction["transaction_index"] if "transaction_index" in transaction else None
    )
    decoded_transaction["status"] = transaction["status"]
    decoded_transaction["contract"] = semantics["contract"]
    decoded_transaction["contract_name"] = semantics["name"]
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
        if block
        else None
    )
    decoded_transaction["l2_to_l1"] = receipt["l2_to_l1_messages"] if receipt else []

    if transaction["transaction"]["type"] == "INVOKE_FUNCTION":
        function_abi = semantics["abi"]["functions"][
            transaction["transaction"]["entry_point_selector"]
        ]
        decoded_transaction["function"] = function_abi["name"]
        decoded_transaction["inputs"] = decode_parameters(
            transaction["transaction"]["calldata"], function_abi["inputs"]
        )
        decoded_transaction["outputs"] = decode_parameters(
            transaction["transaction"].get("outputs", []), function_abi["outputs"]
        )

    return decoded_transaction
