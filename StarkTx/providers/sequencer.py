import requests
from functools import lru_cache

SEQUENCER = 'https://alpha2.starknet.io/feeder_gateway'


# reads block data from the sequencer
@lru_cache()
def get_block(block_id: int) -> dict:
    url = f'{SEQUENCER}/get_block?blockId={block_id}'
    result = requests.get(url).json()
    return result


# reads transaction data from the sequencer
@lru_cache()
def get_transaction(transaction_id: int) -> dict:
    url = f'{SEQUENCER}/get_transaction?transactionId={transaction_id}'
    result = requests.get(url).json()
    return result


# reads the contract data from the sequencer
@lru_cache()
def get_abi(contract_id: str, block_id=None) -> dict:
    url = f'{SEQUENCER}/get_code?contractAddress={contract_id}&blockId={block_id if block_id else "null"}'
    result = requests.get(url).json()
    return result['abi'] if 'abi' in result else dict()
