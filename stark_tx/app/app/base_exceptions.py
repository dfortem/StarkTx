class StarkTxException(Exception):
    ...


class NotSupportedChainError(StarkTxException):
    def __init__(self, chain: str):
        super().__init__(f"{chain.title()} not supported yet.")
