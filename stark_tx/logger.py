import json
import logging
import logging.config
import os

from flask import Flask


def setup_logging(app: Flask):
    """Setup logging"""
    with open(app.config["LOGGING_CONFIG"], "r") as f:
        config = json.load(f)

    config["root"]["level"] = "DEBUG" if app.config["DEBUG"] else "INFO"
    filename = config["handlers"]["file_handler"]["filename"]
    if "/" not in filename:
        log_file_path = os.path.join(app.config["LOGGING_LOG_PATH"], filename)
        os.makedirs(os.path.dirname(log_file_path), exist_ok=True)
        config["handlers"]["file_handler"]["filename"] = log_file_path

    logging.config.dictConfig(config)

    setup_external_logging()


def setup_external_logging() -> None:
    """Setup and override external libs loggers."""
    logging.getLogger("web3").setLevel(logging.INFO)  # web3 logger
