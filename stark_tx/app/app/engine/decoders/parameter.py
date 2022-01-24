from datetime import datetime
from app.engine.providers.semantics import get_semantics


def decode_parameters(chain_id, parameters, parameters_abi):
    decoded_parameters = []
    parameters_index = 0
    abi_index = 0

    while parameters_index < len(parameters):

        parameter_type = (
            "address"
            if "address" in parameters_abi[abi_index]["name"]
            else "timestamp" if "timestamp" in parameters_abi[abi_index]["name"]
               else parameters_abi[abi_index]["type"]
        )

        if parameter_type == "struct":
            name = parameters_abi[abi_index]["name"]
            value, delta = decode_struct(
                              parameters[parameters_index:],
                              parameters_abi[abi_index]["struct_members"]
                           )
            value = "{" + create_parameters_string(value) + "}"
            parameters_index += delta
            abi_index += 1
        elif parameter_type == "struct*":
            name = parameters_abi[abi_index]["name"]
            value = []
            if abi_index > 0 and parameters_abi[abi_index-1]["name"] == parameters_abi[abi_index]["name"] + "_len":
                array_len = decoded_parameters[-1]["value"]
                decoded_parameters.pop()
                value = []
                for _ in range(array_len):
                    fields, delta = decode_struct(
                                        parameters[parameters_index:],
                                        parameters_abi[abi_index]["struct_members"]
                                    )
                    fields = "{" + create_parameters_string(fields) + "}"
                    value.append(fields)
                    parameters_index += delta
            abi_index += 1
        else:
            value = decode_atomic_parameter(
                parameters[parameters_index], parameter_type
            )
            if (
                abi_index + 1 < len(parameters_abi)
                and parameters_abi[abi_index + 1]["type"] == "felt*"
                and parameters_abi[abi_index]["name"]
                == parameters_abi[abi_index + 1]["name"] + "_len"
            ):
                array_len = value
                value = [
                    array_element
                    for array_element in parameters[
                        parameters_index + 1: parameters_index + array_len + 1
                    ]
                ]
                name = parameters_abi[abi_index + 1]["name"]
                parameters_index += array_len + 1
                abi_index += 2
            else:
                name = parameters_abi[abi_index]["name"]
                parameters_index += 1
                abi_index += 1

        decoded_parameters.append(dict(name=name, value=value))

    # simple heuristic to detect internal calls
    if (
        len(decoded_parameters) >= 3
        and decoded_parameters[0]["name"] in ("contract_address", "to")
        and decoded_parameters[1]["name"] in ("function_selector", "selector")
        and decoded_parameters[2]["name"] == "calldata"
    ):
        # these parameters sometimes are a hex string but sometimes are felt
        contract = (
            hex(decoded_parameters[0]["value"])
            if type(decoded_parameters[0]["value"]) == int
            else decoded_parameters[0]["value"]
        )
        selector = (
            hex(decoded_parameters[1]["value"])
            if type(decoded_parameters[1]["value"]) == int
            else decoded_parameters[1]["value"]
        )

        calldata = (
            decoded_parameters[2]["value"]
            if type(decoded_parameters[2]["value"]) == list
            else [decoded_parameters[2]["value"]]
        )

        semantics = get_semantics(chain_id, contract)
        if semantics:
            function_abi = (
                semantics["abi"]["functions"][selector]
                if selector in semantics["abi"]["functions"]
                else None
            )
            if function_abi:
                function_name = function_abi["name"]
                function_inputs = decode_parameters(chain_id, calldata, function_abi["inputs"])
                function_inputs = "{" + create_parameters_string(function_inputs) + "}"
                additional_parameters = decoded_parameters[3:]
                decoded_parameters = [
                    dict(
                        name="contract",
                        value=semantics['name']
                    ),
                    dict(
                        name="function",
                        value=function_name
                    ),
                    dict(
                        name="inputs",
                        value=function_inputs
                    )
                ] + additional_parameters

    return decoded_parameters


def create_parameters_string(parameters):
    parameters_string = ", ".join(
        [
            f"{_input['name']}={_input['value'] if type(_input['value']) != list else '{' + create_parameters_string(_input['value']) + '}'}"
            for _input in parameters
        ]
    )
    return parameters_string


def decode_struct(raw_values, members):
    fields = []
    i = 0
    for member in members:
        field = dict()
        if member["type"] == 'struct':
            field["name"] = member["name"]
            value, delta = decode_struct(
                              raw_values[i:],
                              member["struct_members"],
                            )
            field["value"] = value
            i += delta
        else:
            field["name"] = member["name"]
            field["value"] = decode_atomic_parameter(raw_values[i], member["type"])
            i += 1
        fields.append(field)

    return fields, i


def decode_atomic_parameter(raw_value, parameter_type):
    if parameter_type == "felt":
        parameter_value = int(raw_value)
        if parameter_value > 10**40:
            parameter_value = hex(parameter_value)
    elif parameter_type == "address":
        parameter_value = hex(int(raw_value))
    elif parameter_type == "timestamp":
        parameter_value = str(datetime.fromtimestamp(int(raw_value)))[:19]
    elif parameter_type == "string":
        parameter_value = (
            bytes.fromhex(hex(int(raw_value))[2:]).decode("utf-8").replace("\x00", "")
        )
    else:
        parameter_value = raw_value

    return parameter_value
