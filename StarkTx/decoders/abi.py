import json
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

    return hex(res % ADDRESS_BOUND)


def decode_abi(raw_abi: dict) -> Dict[str, dict]:

    if 'abi' in raw_abi:
        raw_abi = raw_abi['abi']

    structures = dict()
    for element in raw_abi:
        if element['type'] == 'struct':
            structures[element['name']] = [dict(name=member['name'], type=member['type']) for member in element['members']]

    functions = dict()
    l1_handlers = dict()
    for element in raw_abi:
        if element['type'] == 'function':
            selector = get_selector_from_name(element['name'])
            inputs = []
            for _input in element['inputs']:
                if _input['type'] in structures:
                    _input['struct_name'] = _input['type']
                    _input['struct_members'] = structures[_input['struct_name']]
                    _input['type'] = 'struct'
                inputs.append(_input)
            outputs = []
            for _output in element['outputs']:
                if _output['type'] in structures:
                    _output['struct_name'] = _output['type']
                    _output['struct_members'] = structures[_output['struct_name']]
                    _output['type'] = 'struct'
                outputs.append(_output)
            functions[selector] = dict(name=element['name'], inputs=inputs, outputs=outputs)

        elif element['type'] == 'l1_handler':
            selector = get_selector_from_name(element['name'])
            l1_handlers[selector] = dict(name=element['name'], inputs=element['inputs'], outputs=element['outputs'])

    return dict(structures=structures, functions=functions, l1_handlers=l1_handlers)
