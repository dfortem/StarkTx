#  Copyright 2022 Token Flow Insights
#
#  Licensed under the Apache License, Version 2.0 (the "License");
#  you may not use this file except in compliance with the License.
#  You may obtain a copy of the License at: http://www.apache.org/licenses/LICENSE-2.0
#
#  Unless required by applicable law or agreed to in writing, software distributed under
#  the License is distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS
#  OF ANY KIND, either express or implied.
#
#  See the License for the specific language governing permissions and limitations
#  under the License.
#
#  The product contains trademarks and other branding elements of Token Flow Insights SA
#  which are not licensed under the Apache 2.0 license. When using or reproducing the code,
#  please remove the trademark and/or other branding elements.
#

from datetime import datetime


def decode_parameters(chain_id, parameters, parameters_abi):
    decoded_parameters = []
    parameters_index = 0
    abi_index = 0

    while parameters_index < len(parameters) and abi_index < len(parameters_abi):

        parameter_type = (
            "address"
            if "address" in parameters_abi[abi_index]["name"]
            else "timestamp"
            if "timestamp" in parameters_abi[abi_index]["name"]
            else parameters_abi[abi_index]["type"]
        )

        if parameter_type == "struct":
            name = parameters_abi[abi_index]["name"]
            value, delta = decode_struct(
                parameters[parameters_index:],
                parameters_abi[abi_index]["struct_members"],
            )
            value = "{" + create_parameters_string(value) + "}"
            parameters_index += delta
            abi_index += 1

        elif parameter_type == "tuple":
            name = parameters_abi[abi_index]["name"]
            value, delta = decode_struct(
                parameters[parameters_index:],
                parameters_abi[abi_index]["tuple_members"],
            )
            value = "(" + create_parameters_string(value) + ")"
            parameters_index += delta
            abi_index += 1

        elif parameter_type == "struct*":
            name = parameters_abi[abi_index]["name"]
            value = []
            if (
                abi_index > 0
                and parameters_abi[abi_index - 1]["name"]
                == parameters_abi[abi_index]["name"] + "_len"
            ):
                array_len = decoded_parameters[-1]["value"]
                decoded_parameters.pop()
                value = []
                for _ in range(array_len):
                    fields, delta = decode_struct(
                        parameters[parameters_index:],
                        parameters_abi[abi_index]["struct_members"],
                    )
                    fields = "{" + create_parameters_string(fields) + "}"
                    value.append(fields)
                    parameters_index += delta
            abi_index += 1

        elif parameter_type == "tuple*":
            name = parameters_abi[abi_index]["name"]
            value = []
            if (
                abi_index > 0
                and parameters_abi[abi_index - 1]["name"]
                == parameters_abi[abi_index]["name"] + "_len"
            ):
                array_len = decoded_parameters[-1]["value"]
                decoded_parameters.pop()
                value = []
                for _ in range(array_len):
                    fields, delta = decode_struct(
                        parameters[parameters_index:],
                        parameters_abi[abi_index]["tuple_members"],
                    )
                    fields = "(" + create_parameters_string(fields) + ")"
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
                        parameters_index + 1 : parameters_index + array_len + 1
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

    return decoded_parameters


def create_parameters_string(parameters):
    parameters_string = ", ".join(
        [
            f"{_input['name']+'=' if _input['name'] else ''}"
            f"{_input['value'] if type(_input['value']) != list else '{'+create_parameters_string(_input['value'])+'}'}"
            for _input in parameters
        ]
    )
    return parameters_string


def decode_struct(raw_values, members):
    fields = []
    i = 0
    for member in members:
        field = dict()
        if member["type"] == "struct":
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
        if raw_value[:2] == "0x":
            parameter_value = int(raw_value, 16)
        else:
            parameter_value = int(raw_value)
        if parameter_value > 10**40:
            parameter_value = hex(parameter_value)
    elif parameter_type == "address":
        if type(raw_value) == int:
            parameter_value = hex(int(raw_value))
        else:
            parameter_value = raw_value
    elif parameter_type == "timestamp":
        try:
            parameter_value = str(datetime.fromtimestamp(int(raw_value, 16)))[:19]
        except:
            parameter_value = int(raw_value, 16)
    elif parameter_type == "string":
        parameter_value = (
            bytes.fromhex(hex(int(raw_value))[2:]).decode("utf-8").replace("\x00", "")
        )
    else:
        parameter_value = raw_value

    return parameter_value
