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
