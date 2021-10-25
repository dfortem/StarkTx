import os

from dotenv import load_dotenv, find_dotenv

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
load_dotenv(find_dotenv(filename="../.env"))


class Config:
    """Base Config."""

    LOGGING_CONFIG = os.environ.get(
        "LOGGING_CONFIG", os.path.join(BASE_DIR, "../log_cfg.json")
    )
    LOGGING_LOG_PATH = os.environ.get(
        "LOGGING_CONFIG", os.path.join(BASE_DIR, "../tmp")
    )

    API_KEY = os.getenv("API_KEY", "")
    MAX_CONTENT_LENGTH = 10 * 1024 * 1024


class ProductionConfig(Config):
    """Production Config."""

    ENV = "production"
    FLASK_DEBUG = False
    TESTING = False
    PROPAGATE_EXCEPTIONS = True


class StagingConfig(Config):
    """Staging Config."""

    ENV = "staging"
    FLASK_DEBUG = True
    TESTING = False
    PROPAGATE_EXCEPTIONS = True


class DevelopmentConfig(Config):
    """Development Config."""

    ENV = "development"
    FLASK_DEBUG = True
    TESTING = True
    PROPAGATE_EXCEPTIONS = True
