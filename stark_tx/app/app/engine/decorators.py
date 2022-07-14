#  Copyright 2022 Token Flow Insights
#
#  Licensed under the Apache License, Version 2.0 (the "License");
#  you may not use this file except in compliance with the License.
#  You may obtain a copy of the License at: http://www.apache.org/licenses/LICENSE-2.0
#
#  Unless required by applicable law or agreed to in writing, software distributed under
#  the License is distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS
#  OF ANY KIND, either express or implied.
#
#  See the License for the specific language governing permissions and limitations
#  under the License.
#
#  The product contains trademarks and other branding elements of Token Flow Insights SA
#  which are not licensed under the Apache 2.0 license. When using or reproducing the code,
#  please remove the trademark and/or other branding elements.
#

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
    """StarkNet API handler."""

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
