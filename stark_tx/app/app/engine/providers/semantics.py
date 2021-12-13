import json
from typing import Optional

from app.engine.decoders.abi import decode_abi
from app.engine.providers.sequencer import get_abi

semantics = {}


def load_semantics():
    global semantics
    try:
        semantics = json.load(open("artefacts/semantics.json", "r"))
    except Exception:
        pass


def store_semantics():
    global semantics
    json.dump(semantics, open("artefacts/semantics.json", "w"))


def get_semantics(contract: str, block_hash: Optional[str] = None) -> dict:
    global semantics

    if contract in semantics:
        contract_semantics = semantics[contract]
    else:
        raw_abi = get_abi(contract, block_hash=block_hash)
        decoded_abi = decode_abi(raw_abi["abi"] if "abi" in raw_abi else {})
        contract_semantics = dict(
            contract=contract, name=contract[:10], abi=decoded_abi
        )
        semantics[contract] = contract_semantics

    return contract_semantics
