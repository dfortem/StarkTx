import logging
from functools import lru_cache
from typing import Optional

import requests

from app.core.config import SequencerURL
from app.engine.decorators import starknet_api_handler
from app.engine.types import TStarkNetAPIResponse

logger = logging.getLogger(__name__)


# reads block data from the sequencer
@lru_cache()
@starknet_api_handler
def get_block(chain_id: str, block_id: int) -> TStarkNetAPIResponse:
    url = f"{SequencerURL[chain_id]}/get_block?blockHash={block_id}"
    logger.info("Get_block url: %s", url)

    return requests.get(url)


# reads transaction data from the sequencer
@lru_cache()
@starknet_api_handler
def get_transaction(chain_id: str, transaction_hash: str) -> TStarkNetAPIResponse:
    url = f"{SequencerURL[chain_id]}/get_transaction?transactionHash={transaction_hash}"
    logger.info("Get_transaction: url: %s", url)

    return requests.get(url)


# reads the contract data from the sequencer
@lru_cache()
@starknet_api_handler
def get_abi(
    chain_id: str, contract_id: str, *, block_hash: Optional[str] = None
) -> TStarkNetAPIResponse:
    url = (
        f"{SequencerURL[chain_id]}/get_code?"
        f'contractAddress={contract_id}{"&blockHash=" + block_hash if block_hash and block_hash != "pending" else ""}'
    )
    logger.info("Get_abi: url: %s", url)

    return requests.get(url)
