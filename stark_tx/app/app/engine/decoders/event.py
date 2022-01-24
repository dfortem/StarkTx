from app.engine.decoders.parameter import decode_parameters


def decode_event(chain_id, event, event_abi):
    parameters = decode_parameters(chain_id, event["data"], event_abi['parameters'] if event_abi else [])
    decoded_event = dict(contract=event['from_address'], name=event_abi['name'] if event_abi else "",
                         keys=event['keys'], parameters=parameters)

    return decoded_event
