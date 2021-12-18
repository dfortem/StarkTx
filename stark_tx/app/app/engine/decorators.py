from typing import Callable
from functools import wraps

from requests import HTTPError

from app.engine.types import TStarkNetAPIHandler, TStarkNetAPIResponse


def starknet_api_handler(
    func: Callable[..., TStarkNetAPIHandler]
) -> Callable[..., TStarkNetAPIHandler]:
    """ StarkNet API handler."""

    @wraps(func)
    def wrapped(*args, **kwargs) -> TStarkNetAPIResponse:
        try:
            response = func(*args, **kwargs)
            response.raise_for_status()
            return response.json()
        except HTTPError as e:
            raise HTTPError(response=e.response)

    return wrapped
