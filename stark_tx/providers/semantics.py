import json

from stark_tx.providers.sequencer import get_abi
from stark_tx.decoders.abi import decode_abi


semantics = dict()


def load_semantics():
    global semantics
    try:
        semantics = json.load(open("artefacts/semantics.json", "r"))
    except Exception:
        pass


def store_semantics():
    global semantics
    json.dump(semantics, open("artefacts/semantics.json", "w"))


def get_semantics(contract: str) -> dict:

    global semantics

    if contract in semantics:
        contract_semantics = semantics[contract]
    else:
        raw_abi = get_abi(contract)
        decoded_abi = decode_abi(raw_abi)
        contract_semantics = dict(
            contract=contract, name=contract[:10], abi=decoded_abi
        )
        semantics[contract] = contract_semantics

    return contract_semantics
