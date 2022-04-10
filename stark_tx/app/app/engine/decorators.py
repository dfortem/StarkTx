from functools import wraps
from typing import Callable

from requests import HTTPError

from app.base_exceptions import TransactionStatusError
from app.engine.providers.status import SequencerStatus
from app.engine.types import TStarkNetAPIHandler, TStarkNetAPIResponse


# TODO: definitely handle these trash requests exceptions
def starknet_api_handler(
    func: Callable[..., TStarkNetAPIHandler]
) -> Callable[..., TStarkNetAPIHandler]:
    """ StarkNet API handler."""

    @wraps(func)
    def wrapped(*args, **kwargs) -> TStarkNetAPIResponse:
        try:
            response = func(*args, **kwargs)
            response.raise_for_status()

            json = response.json()

            if json.get("status") and json["status"] in SequencerStatus:
                if SequencerStatus[json["status"]].value[0] is False:
                    raise TransactionStatusError(json["status"])

            return json
        except HTTPError as e:
            raise HTTPError(response=e.response)

    return wrapped
