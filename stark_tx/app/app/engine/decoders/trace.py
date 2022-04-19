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

from app.engine.decoders.parameter import decode_parameters
from app.engine.decoders.event import decode_event
from app.engine.providers.semantics import get_semantics


def decode_trace(chain_id: str, block_hash: str, trace: dict, trace_id: str or None, indent: int) -> tuple:

    semantics = get_semantics(
        chain_id,
        trace["code_address"],
        block_hash,
    )

    decoded_trace = dict()
    decoded_trace["trace_id"] = trace_id
    decoded_trace["type"] = 'DEPLOY' if trace["entry_point_type"] == 'CONSTRUCTOR' else 'INVOKE_FUNCTION'
    decoded_trace["entry_point_type"] = trace["entry_point_type"]
    decoded_trace["caller"] = trace["caller_address"]
    decoded_trace["contract"] = trace["code_address"]

    if decoded_trace["type"] == "INVOKE_FUNCTION":

        decoded_trace["code"] = trace["code_address"]

        decoded_trace['entry_point_selector'] = trace["selector"]
        decoded_trace['entry_point_type'] = trace["entry_point_type"]

        function_abi = semantics["abi"]["functions"].get(trace["selector"])
        if not function_abi and '__default__' in semantics["abi"]["functions"]:
            function_abi = semantics["abi"]["functions"]['__default__']
            if function_abi['inputs'][1]['name'] == 'calldata_size' or \
               (len(trace['calldata']) > 2 and int(trace['calldata'][1], 16) != len(trace['calldata']) - 2):
                trace['calldata'].insert(0, hex(len(trace["calldata"])))
                trace['calldata'].insert(0, trace["selector"])
                function_abi['inputs'][1]['name'] = 'calldata_len'
            if function_abi['outputs'][0]['name'] == 'retdata_size' or \
               (len(trace['result']) > 0 and int(trace['result'][0], 16) != len(trace['result']) - 2):
                function_abi['outputs'][0]['name'] = 'retdata_len'
                trace['result'].insert(0, hex(len(trace["result"])))

        if function_abi:
            decoded_trace["function"] = function_abi["name"]
            decoded_trace["inputs"] = decode_parameters(
                chain_id,
                trace["calldata"],
                function_abi["inputs"]
            )
            decoded_trace["outputs"] = decode_parameters(
                chain_id,
                trace.get("result", []),
                function_abi["outputs"],
            )
        else:
            decoded_trace["function"] = trace["selector"]
            decoded_trace["inputs"] = \
                [dict(name=f'input_{i}', value=value)
                 for i, value in enumerate(trace["calldata"])]
            decoded_trace["outputs"] = \
                [dict(name=f'output_{i}', value=value)
                 for i, value in enumerate(trace.get("result", []))]

    elif decoded_trace["type"] == "DEPLOY":

        decoded_trace['entry_point_selector'] = "constructor"
        decoded_trace['entry_point_type'] = "CONSTRUCTOR"

        if "constructor" in semantics["abi"]["functions"]:
            function_abi = semantics["abi"]["functions"]["constructor"]
            decoded_trace["function"] = function_abi["name"]
            decoded_trace["inputs"] = decode_parameters(
                chain_id,
                trace['calldata'],
                function_abi["inputs"]
            )
            decoded_trace["outputs"] = []
        else:
            decoded_trace["function"] = None
            decoded_trace["inputs"] = []
            decoded_trace["outputs"] = []

    else:
        print("Unknown type...")

    decoded_events = []
    if 'events' in trace:
        for event in trace['events']:
            if len(event['keys']):
                if type(event['keys'][0]) == int:
                    selector = hex(int(event['keys'][0]))
                else:
                    selector = event['keys'][0]
                event_abi = semantics["abi"]["events"].get(selector)
            else:
                event_abi = None
            decoded_events.append(decode_event(chain_id, trace['contract_address'], event, event_abi))

    decoded_trace['calls'] = []
    for i, sub_trace in enumerate(trace['internal_calls']):
        sub_trace_id = trace_id + '_' if trace_id else ''
        sub_trace_id += str(i)
        sub_calls, sub_events = decode_trace(chain_id, block_hash, sub_trace, sub_trace_id, indent + 1)
        decoded_trace['calls'].append(sub_calls)
        decoded_events += sub_events

    decoded_trace['execution_resources'] = trace.get('execution_resources', [])
    decoded_trace['indent'] = indent

    return decoded_trace, decoded_events
