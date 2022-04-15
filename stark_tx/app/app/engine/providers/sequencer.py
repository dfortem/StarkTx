#   Copyright 2022 Token Flow Insights
#
#   Licensed under the Apache License, Version 2.0 (the "License");
#   you may not use this file except in compliance with the License.
#   You may obtain a copy of the License at: http://www.apache.org/licenses/LICENSE-2.0
#
#   Unless required by applicable law or agreed to in writing, software
#   distributed under the License is distributed on an "AS IS" BASIS,
#   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#   See the License for the specific language governing permissions and
#   limitations under the License.
#
#

import logging
from functools import lru_cache
from typing import Optional

import requests

from app.core.config import SequencerURL
from app.engine.decorators import starknet_api_handler
from app.engine.types import TStarkNetAPIResponse

logger = logging.getLogger(__name__)


# reads block data from the sequencer (by hash)
@lru_cache()
@starknet_api_handler
def get_block_hash(chain_id: str, block_hash: int) -> TStarkNetAPIResponse:
    url = f"{SequencerURL[chain_id]}/get_block?blockHash={block_hash}"
    logger.info("Get_block url: %s", url)

    return requests.get(url)


# reads block data from the sequencer (by id)
@lru_cache()
@starknet_api_handler
def get_block_id(chain_id: str, block_id: int) -> TStarkNetAPIResponse:
    url = f"{SequencerURL[chain_id]}/get_block?blockNumber={block_id}"
    logger.info("Get_block url: %s", url)

    return requests.get(url)


# reads transaction data from the sequencer
@lru_cache()
@starknet_api_handler
def get_transaction(chain_id: str, transaction_hash: str) -> TStarkNetAPIResponse:
    url = f"{SequencerURL[chain_id]}/get_transaction?transactionHash={transaction_hash}"
    logger.info("Get_transaction: url: %s", url)

    return requests.get(url)


# reads transaction trace data from the sequencer
@lru_cache()
@starknet_api_handler
def get_transaction_trace(chain_id: str, transaction_hash: str) -> TStarkNetAPIResponse:
    url = f"{SequencerURL[chain_id]}/get_transaction_trace?transactionHash={transaction_hash}"
    logger.info("Get_transaction trace: url: %s", url)

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
