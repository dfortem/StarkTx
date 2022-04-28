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

import secrets
from enum import Enum, EnumMeta

from pydantic import AnyHttpUrl, BaseSettings

from app.base_exceptions import NotSupportedChainError


class Settings(BaseSettings):

    SECRET_KEY: str = secrets.token_urlsafe(32)
    # 60 minutes * 24 hours * 8 days
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 8

    # StarkNet environments
    SEQUENCERS = dict()
    SEQUENCERS['mainnet']: AnyHttpUrl = "https://alpha-mainnet.starknet.io/feeder_gateway"
    SEQUENCERS['testnet']: AnyHttpUrl = "https://alpha4.starknet.io/feeder_gateway"
    SEQUENCERS['integration']: AnyHttpUrl = "https://external.integration.starknet.io/feeder_gateway"

    DEFAULT_SEQUENCER_URL: AnyHttpUrl = SEQUENCERS['mainnet']

    PROJECT_NAME: str

    class Config:
        case_sensitive = True
        use_enum_values = True


settings = Settings()


class EnumValidator(EnumMeta):
    def __getitem__(cls, name):
        try:
            if not name:
                return super().__getitem__("DEFAULT")
            return super().__getitem__(name)
        except KeyError:
            raise NotSupportedChainError(name)


class SequencerURL(str, Enum, metaclass=EnumValidator):

    DEFAULT = settings.DEFAULT_SEQUENCER_URL

    mainnet = settings.SEQUENCERS['mainnet']
    testnet = settings.SEQUENCERS['testnet']
    integration = settings.SEQUENCERS['integration']
