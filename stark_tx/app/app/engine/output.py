import logging

log = logging.getLogger(__name__)


def print_transaction(tx):
    log.info(
        "Block: %s/%s Time: %s", tx["block_hash"], tx["block_number"], tx["timestamp"]
    )
    log.info(
        "Tx: %s Index: %s Status: %s",
        tx["transaction_hash"],
        tx["transaction_index"],
        tx["status"],
    )
    if tx["type"] == "INVOKE_FUNCTION":
        input_string = ", ".join(
            [f"{_input['name']}={_input['value']}" for _input in tx["inputs"]]
        )
        output_string = ", ".join(
            [f"{_output['name']}={_output['value']}" for _output in tx["outputs"]]
        )
        log.info(
            "Invoke %s.%s(%s) -> (%s)",
            tx["contract_name"],
            tx["function"],
            input_string,
            output_string,
        )
    elif tx["type"] == "DEPLOY":
        log.info("Deploy %s", tx["contract"])
    for transaction in tx["l2_to_l1"]:
        payload_string = ", ".join(transaction["payload"])
        log.info(
            "L2->L1: %s -> %s (%s)",
            transaction["from_address"],
            transaction["to_address"],
            payload_string,
        )

    return
