from typing import Dict

from eth_hash.auto import keccak
from starkware.cairo.lang.vm.crypto import pedersen_hash

MAX_STORAGE_ITEM_SIZE = 256
ADDRESS_BOUND = 2 ** 251 - MAX_STORAGE_ITEM_SIZE
MASK_250 = 2 ** 250 - 1


def starknet_keccak(data: bytes) -> int:
    return int.from_bytes(keccak(data), "big") & MASK_250


def get_selector_from_name(func_name: str) -> str:
    return hex(starknet_keccak(data=func_name.encode("ascii")))


def get_storage_var_address(var_name: str, *args) -> str:
    res = starknet_keccak(var_name.encode("utf8"))
    for arg in args:
        assert isinstance(arg, int), f"Expected arguments to be integers. Found: {arg}."
        res = pedersen_hash(res, arg)
    address = hex(res % ADDRESS_BOUND)
    address = '0x' + '0'*(64 - len(address[2:])) + address[2:]

    return address


def decode_abi(raw_abi: dict) -> Dict[str, dict]:

    def _flatten_parameters(_parameters, _structures):
        flattened_parameters = []
        for _parameter in _parameters:
            _parameter["type"] = _parameter["type"].strip()
            if _parameter["type"][0] == "(" and _parameter["type"][-1] == ")":
                _parameter["tuple_members"] = []
                for _tuple_item in _parameter["type"][1:-1].split(','):
                    _parameter["tuple_members"] += _flatten_parameters([dict(name="", type=_tuple_item)], _structures)
                _parameter["type"] = "tuple"
            elif _parameter["type"][0] == "(" and _parameter["type"][-2:] == ")*":
                _parameter["tuple_members"] = []
                for _tuple_item in _parameter["type"][1:-2].split(','):
                    _parameter["tuple_members"] += _flatten_parameters([dict(name="", type=_tuple_item)], _structures)
                _parameter["type"] = "tuple*"
            elif _parameter["type"] in _structures:
                _parameter["struct_name"] = _parameter["type"]
                _parameter["struct_members"] = _flatten_parameters(_structures[_parameter["struct_name"]], _structures)
                _parameter["type"] = "struct"
            elif _parameter["type"][-1:] == '*' and _parameter["type"][:-1] in _structures:
                _parameter["struct_name"] = _parameter["type"][:-1]
                _parameter["struct_members"] = _flatten_parameters(_structures[_parameter["struct_name"]], _structures)
                _parameter["type"] = "struct*"
            flattened_parameters.append(_parameter)
        return flattened_parameters

    if "abi" in raw_abi:
        raw_abi = raw_abi["abi"]

    structures = dict()
    for element in raw_abi:
        if element["type"] == "struct":
            structures[element["name"]] = [
                dict(name=member["name"], type=member["type"])
                for member in element["members"]
            ]

    functions = dict()
    events = dict()
    l1_handlers = dict()
    for element in raw_abi:

        if element["type"] == "constructor":
            inputs = _flatten_parameters(element["inputs"], structures)
            functions['constructor'] = dict(
                name=element["name"], inputs=inputs, outputs=dict()
            )

        elif element["type"] == "function":
            selector = get_selector_from_name(element["name"]) \
                if element["name"] != "__default__" else element["name"]
            inputs = _flatten_parameters(element["inputs"], structures)
            outputs = _flatten_parameters(element["outputs"], structures)
            functions[selector] = dict(
                name=element["name"], inputs=inputs, outputs=outputs
            )

        elif element["type"] == "event":
            selector = get_selector_from_name(element["name"])
            parameters = _flatten_parameters(element["data"], structures)
            events[selector] = dict(
                name=element["name"], keys=element["keys"], parameters=parameters
            )

        elif element["type"] == "l1_handler":
            selector = get_selector_from_name(element["name"]) \
                if element["name"] != "__l1_default__" else element["name"]
            inputs = _flatten_parameters(element["inputs"], structures)
            outputs = _flatten_parameters(element["outputs"], structures)
            l1_handlers[selector] = dict(name=element["name"], inputs=inputs, outputs=outputs)

    return dict(structures=structures, functions=functions, events=events, l1_handlers=l1_handlers)
