from functools import lru_cache
from typing import Optional

import requests

from app.core.config import settings


# reads block data from the sequencer
@lru_cache()
def get_block(block_id: int) -> dict:
    url = f"{settings.SEQUENCER}/get_block?blockHash={block_id}"
    result = requests.get(url).json()
    return result


# reads transaction data from the sequencer
@lru_cache()
def get_transaction(transaction_hash: str) -> dict:
    url = f"{settings.SEQUENCER}/get_transaction?transactionHash={transaction_hash}"
    result = requests.get(url).json()
    return result


# reads the contract data from the sequencer
@lru_cache()
def get_abi(contract_id: str, *, block_hash: Optional[str] = None) -> dict:
    url = (
        f"{settings.SEQUENCER}/get_code?"
        f'contractAddress={contract_id}&blockHash={block_hash if block_hash else "null"}'
    )
    result = requests.get(url).json()
    return result["abi"] if "abi" in result else {}
