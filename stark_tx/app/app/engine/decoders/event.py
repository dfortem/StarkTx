from app.engine.decoders.parameter import decode_parameters


def decode_event(chain_id, event, event_abi):
    if event_abi and 'parameters' in event_abi:
        parameters = decode_parameters(chain_id, event["data"], event_abi['parameters'])
    else:
        parameters = [dict(name=f'data_{i}', value=event['data'][i]) for i in range(len(event['data']))]

    decoded_event = dict(contract=event['from_address'], name=event_abi['name'] if event_abi else "anonymous",
                         keys=event['keys'], parameters=parameters)

    return decoded_event
