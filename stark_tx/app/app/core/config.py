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
    SEQUENCERS['hackathon_0']: AnyHttpUrl = "https://hackathon-0.starknet.io/feeder_gateway"
    SEQUENCERS['hackathon_1']: AnyHttpUrl = "https://hackathon-1.starknet.io/feeder_gateway"
    SEQUENCERS['hackathon_2']: AnyHttpUrl = "https://hackathon-2.starknet.io/feeder_gateway"
    SEQUENCERS['hackathon_3']: AnyHttpUrl = "https://hackathon-3.starknet.io/feeder_gateway"
    SEQUENCERS['hackathon_4']: AnyHttpUrl = "https://hackathon-4.starknet.io/feeder_gateway"
    SEQUENCERS['hackathon_5']: AnyHttpUrl = "https://hackathon-5.starknet.io/feeder_gateway"
    SEQUENCERS['hackathon_6']: AnyHttpUrl = "https://hackathon-6.starknet.io/feeder_gateway"
    SEQUENCERS['hackathon_7']: AnyHttpUrl = "https://hackathon-7.starknet.io/feeder_gateway"
    SEQUENCERS['hackathon_8']: AnyHttpUrl = "https://hackathon-8.starknet.io/feeder_gateway"
    SEQUENCERS['hackathon_9']: AnyHttpUrl = "https://hackathon-9.starknet.io/feeder_gateway"

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
    hackathon_0 = settings.SEQUENCERS['hackathon_0']
    hackathon_1 = settings.SEQUENCERS['hackathon_1']
    hackathon_2 = settings.SEQUENCERS['hackathon_2']
    hackathon_3 = settings.SEQUENCERS['hackathon_3']
    hackathon_4 = settings.SEQUENCERS['hackathon_4']
    hackathon_5 = settings.SEQUENCERS['hackathon_5']
    hackathon_6 = settings.SEQUENCERS['hackathon_6']
    hackathon_7 = settings.SEQUENCERS['hackathon_7']
    hackathon_8 = settings.SEQUENCERS['hackathon_8']
    hackathon_9 = settings.SEQUENCERS['hackathon_9']
