def print_transaction(tx):
    print()
    print(f"Block: {tx['block_id']}/{tx['block_number']} Time: {tx['timestamp']}")
    print(
        f"Tx: {tx['transaction_id']} Index: {tx['transaction_index']} Status: {tx['status']}"
    )
    if tx["type"] == "INVOKE_FUNCTION":
        input_string = ", ".join(
            [f"{_input['name']}={_input['value']}" for _input in tx["inputs"]]
        )
        output_string = ", ".join(
            [f"{_output['name']}={_output['value']}" for _output in tx["outputs"]]
        )
        print(
            f"Invoke {tx['contract_name']}.{tx['function']}({input_string}) -> ({output_string})"
        )
    elif tx["type"] == "DEPLOY":
        print(f"Deploy {tx['contract']}")
    for transaction in tx["l2_to_l1"]:
        payload_string = ", ".join(transaction["payload"])
        print(
            f"L2->L1: {transaction['from_address']} -> {transaction['to_address']} ({payload_string})"
        )

    return
