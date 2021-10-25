from datetime import datetime

from stark_tx.providers.semantics import get_semantics
from stark_tx.decoders.parameter import decode_parameters


def decode_transaction(block: dict, transaction: dict) -> dict:

    semantics = get_semantics(transaction["transaction"]["contract_address"])

    decoded_transaction = dict()
    decoded_transaction["block_id"] = (
        transaction["block_id"] if "block_id" in transaction else None
    )
    decoded_transaction["block_number"] = (
        transaction["block_number"] if "block_number" in transaction else None
    )
    decoded_transaction["timestamp"] = (
        datetime.fromtimestamp(block["timestamp"])
        if block and "timestamp" in block
        else None
    )
    decoded_transaction["transaction_id"] = transaction["transaction_id"]
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
        block["transaction_receipts"].get(str(transaction["transaction_id"]))
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
