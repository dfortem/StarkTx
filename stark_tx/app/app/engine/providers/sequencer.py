from functools import lru_cache
from typing import Optional

import requests
from requests import Response

from app.core.config import settings

from app.engine.decorators import starknet_api_handler


# reads block data from the sequencer
@lru_cache()
@starknet_api_handler
def get_block(block_id: int) -> Response:
    url = f"{settings.SEQUENCER}/get_block?blockHash={block_id}"
    return requests.get(url)


# reads transaction data from the sequencer
@lru_cache()
@starknet_api_handler
def get_transaction(transaction_hash: str) -> Response:
    url = f"{settings.SEQUENCER}/get_transaction?transactionHash={transaction_hash}"
    return requests.get(url)


# reads the contract data from the sequencer
@lru_cache()
@starknet_api_handler
def get_abi(contract_id: str, *, block_hash: Optional[str] = None) -> Response:
    url = (
        f"{settings.SEQUENCER}/get_code?"
        f'contractAddress={contract_id}&blockHash={block_hash if block_hash else "null"}'
    )
    return requests.get(url)
