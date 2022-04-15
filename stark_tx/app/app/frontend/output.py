#   Copyright 2022 Token Flow Insights
#
#   Licensed under the Apache License, Version 2.0 (the "License");
#   you may not use this file except in compliance with the License.
#   You may obtain a copy of the License at: http://www.apache.org/licenses/LICENSE-2.0
#
#   Unless required by applicable law or agreed to in writing, software
#   distributed under the License is distributed on an "AS IS" BASIS,
#   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#   See the License for the specific language governing permissions and
#   limitations under the License.
#
#

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
            tx["contract"],
            tx["function"],
            input_string,
            output_string,
        )
    elif tx["type"] == "DEPLOY":
        log.info("Deploy %s", tx["contract"])
        input_string = ", ".join(
            [f"{_input['name']}={_input['value']}" for _input in tx["inputs"]]
        )
    for transaction in tx["l2_to_l1_messages"]:
        payload_string = ", ".join(transaction["payload"])
        log.info(
            "L2->L1: %s -> %s (%s)",
            transaction["from_address"],
            transaction["to_address"],
            payload_string,
        )

    return
