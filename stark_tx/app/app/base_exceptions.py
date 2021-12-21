class StarkTxException(Exception):
    ...


class NotSupportedChainError(StarkTxException):
    def __init__(self, chain: str):
        super().__init__(f"{chain.title()} not supported yet.")


class StarkNetAPIError(StarkTxException):
    ...


class TransactionStatusError(StarkTxException):
    def __init__(self, msg: str):
        super().__init__(msg.replace("_", " ").lower().capitalize())
