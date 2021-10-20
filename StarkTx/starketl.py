import pickle

from StarkTx.providers.sequencer import get_block, get_transaction
from StarkTx.providers.semantics import load_semantics, store_semantics
from StarkTx.decoders.transaction import decode_transaction
from StarkTx.templates.output import print_transaction


def starktx_transaction(transaction_id: int) -> dict:

    raw_transaction = get_transaction(transaction_id)
    raw_block = get_block(raw_transaction['block_id']) if 'block_id' in raw_transaction else None
    decoded_transaction = decode_transaction(raw_block, raw_transaction)
    print_transaction(decoded_transaction)

    return decoded_transaction


def starktx_block(block_id: int) -> []:

    raw_block = get_block(block_id)
    decoded_transactions = []
    for index, (transaction_id, block_transaction) in enumerate(raw_block['transactions'].items()):
        raw_transaction = dict()
        raw_transaction['transaction_id'] = int(transaction_id)
        raw_transaction['transaction_index'] = index
        raw_transaction['block_id'] = block_id
        raw_transaction['block_number'] = raw_block['sequence_number']
        raw_transaction['status'] = raw_block['status']
        raw_transaction['transaction'] = block_transaction

        decoded_transaction = decode_transaction(raw_block, raw_transaction)
        decoded_transactions.append(decoded_transaction)

        print_transaction(decoded_transaction)

    return decoded_transactions


def store_transactions(batch: [], block: int):
    pickle.dump(batch, open(f'artefacts/blocks_{block}.pickle', 'wb'))


load_semantics()

min_block = 6300
max_block = 48200
chunk_size = 100
for start_block in range(min_block, max_block, chunk_size):
    transactions_batch = []
    for block_id in range(start_block, start_block + chunk_size):
        transactions_batch += starktx_block(block_id)
    store_transactions(transactions_batch, start_block)
    store_semantics()

store_semantics()

# failed transaction: 260219
