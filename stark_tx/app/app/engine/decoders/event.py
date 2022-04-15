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


def decode_event(chain_id, contract, event, event_abi):
    if event_abi and 'parameters' in event_abi:
        parameters = decode_parameters(chain_id, event["data"], event_abi['parameters'])
    else:
        parameters = [dict(name=f'key_{i}', value=event['keys'][i]) for i in range(len(event['keys']))] + \
                     [dict(name=f'data_{i}', value=event['data'][i]) for i in range(len(event['data']))]

    decoded_event = dict(contract=contract, name=event_abi['name'] if event_abi else "anonymous",
                         keys=event['keys'], parameters=parameters, order=event['order'])

    return decoded_event
