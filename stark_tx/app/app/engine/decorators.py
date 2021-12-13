from collections import Callable
from functools import wraps

from requests import HTTPError


def starknet_api_handler(func: Callable):
    """ StarkNet API handler."""

    @wraps(func)
    def wrapped(*args, **kwargs):
        try:
            response = func(*args, **kwargs)
            response.raise_for_status()
            return response
        except HTTPError as e:
            raise HTTPError(response=e.response)

    return wrapped
