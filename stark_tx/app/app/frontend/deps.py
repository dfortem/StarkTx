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

import re

from flask import request


def extract_tx_hash_from_req() -> str:
    """Extract tx hash from request url."""
    hash_match = re.findall(r"(0x)?([A-Fa-f0-9]{63})", request.url)

    return (
        f"{hash_match[0][0]}{hash_match[0][1]}"
        if hash_match and len(hash_match[0]) == 2
        else ""
    )
