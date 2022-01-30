from datetime import datetime

from app.engine.decoders.parameter import decode_parameters
from app.engine.decoders.event import decode_event
from app.engine.providers.semantics import get_semantics


def decode_transaction(chain_id: str, block: dict, transaction: dict) -> dict:

    semantics = get_semantics(
        chain_id,
        transaction["transaction"]["contract_address"],
        transaction["block_hash"],
    )

    decoded_transaction = dict()
    decoded_transaction["chain_id"] = chain_id
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
    decoded_transaction["contract"] = semantics["contract"]
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

    decoded_transaction['events'] = []
    if receipt and 'events' in receipt:
        for event in receipt['events']:
            event_semantics = get_semantics(chain_id, event["from_address"], transaction["block_hash"])
            if len(event['keys']):
                selector = hex(int(event['keys'][0]))
                event_abi = event_semantics["abi"]["events"].get(selector)
            else:
                event_abi = None
            decoded_transaction['events'].append(decode_event(chain_id, event, event_abi))

    decoded_transaction['l2_to_l1_messages'] = receipt['l2_to_l1_messages'] if receipt else []

    if transaction["transaction"]["type"] == "INVOKE_FUNCTION":

        decoded_transaction['entry_point_selector'] = transaction["transaction"]["entry_point_selector"]
        decoded_transaction['entry_point_type'] = transaction["transaction"]["entry_point_type"]

        if decoded_transaction['entry_point_type'] == 'L1_HANDLER':
            function_abi = semantics["abi"]["l1_handlers"].get(transaction["transaction"]["entry_point_selector"])
        else:
            function_abi = semantics["abi"]["functions"].get(transaction["transaction"]["entry_point_selector"])

        if not function_abi:
            if decoded_transaction['entry_point_type'] == 'L1_HANDLER':
                function_abi = semantics["abi"]["l1_handlers"].get("__l1_default__")
            else:
                function_abi = semantics["abi"]["functions"].get("__default__")

        if function_abi:
            decoded_transaction["function"] = function_abi["name"]
            decoded_transaction["inputs"] = decode_parameters(
                chain_id,
                transaction["transaction"]["calldata"],
                function_abi["inputs"]
            )
            decoded_transaction["outputs"] = decode_parameters(
                chain_id,
                transaction["transaction"].get("outputs", []),
                function_abi["outputs"],
            )
        else:
            decoded_transaction["function"] = transaction["transaction"]["entry_point_selector"]
            decoded_transaction["inputs"] = \
                [dict(name=f'input_{i}', value=value)
                 for i, value in enumerate(transaction["transaction"]["calldata"])]
            decoded_transaction["outputs"] = \
                [dict(name=f'input_{i}', value=value)
                 for i, value in enumerate(transaction["transaction"].get("outputs", []))]

    elif transaction["transaction"]["type"] == "DEPLOY":

        decoded_transaction['entry_point_selector'] = "constructor"
        decoded_transaction['entry_point_type'] = "CONSTRUCTOR"

        if "constructor" in semantics["abi"]["functions"]:
            function_abi = semantics["abi"]["functions"]["constructor"]
            decoded_transaction["function"] = function_abi["name"]
            decoded_transaction["inputs"] = decode_parameters(
                chain_id,
                transaction["transaction"]['constructor_calldata'],
                function_abi["inputs"]
            )
            decoded_transaction["outputs"] = []
        else:
            decoded_transaction["function"] = None
            decoded_transaction["inputs"] = []
            decoded_transaction["outputs"] = []

    decoded_transaction['execution_resources'] = receipt['execution_resources'] if receipt else []

    return decoded_transaction
