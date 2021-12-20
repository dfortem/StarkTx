import secrets
from enum import Enum, EnumMeta

from pydantic import AnyHttpUrl, BaseSettings

from app.base_exceptions import NotSupportedChainError


class Settings(BaseSettings):
    SECRET_KEY: str = secrets.token_urlsafe(32)
    # 60 minutes * 24 hours * 8 days = 8 days
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 8

    # StarkWare
    SEQUENCER_ETH_MAINNET: AnyHttpUrl = "https://alpha-mainnet.starknet.io/feeder_gateway"
    SEQUENCER_GOERLI_TESTNET: AnyHttpUrl = "https://alpha4.starknet.io/feeder_gateway"

    PROJECT_NAME: str

    class Config:
        case_sensitive = True
        use_enum_values = True


settings = Settings()


class EnumValidator(EnumMeta):
    def __getitem__(cls, name):
        if name.lower() == "mainnet":
            raise NotSupportedChainError(name)
        return super().__getitem__(name)


class SequencerURL(str, Enum, metaclass=EnumValidator):
    mainnet = settings.SEQUENCER_ETH_MAINNET
    goerli = settings.SEQUENCER_GOERLI_TESTNET
