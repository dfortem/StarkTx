import logging
from functools import wraps
from typing import Callable, Optional

from flask import Blueprint, render_template
from requests import HTTPError
from werkzeug.exceptions import HTTPException

from app.base_exceptions import NotSupportedChainError
from app.frontend.deps import extract_tx_hash_from_req

log = logging.getLogger(__name__)

exceptions_bp = Blueprint("exceptions", __name__)


def render_error_page(status: Optional[int] = 500):
    """Render error page."""

    def _render_error_page(f: Callable):
        @wraps(f)
        def wrapper(*args, **kwargs):
            error = f(*args, **kwargs)
            status_code = status
            if isinstance(error, HTTPException):
                error, status_code = error.description, error.code
            elif isinstance(error, HTTPError):
                error, status_code = (
                    error.response.json()["message"],
                    error.response.status_code,
                )
            return (
                render_template(
                    "exception.html",
                    status_code=status_code,
                    error=error,
                    tx_hash=extract_tx_hash_from_req(),
                ),
                status_code,
            )

        return wrapper

    return _render_error_page


@exceptions_bp.app_errorhandler(HTTPException)
@render_error_page()
def handle_all_http_exceptions(error: HTTPException) -> HTTPException:
    """All HTTP Exceptions handler."""
    return error


@exceptions_bp.app_errorhandler(NotSupportedChainError)
@render_error_page(status=501)
def handle_not_supported_chain_error(error: NotSupportedChainError) -> str:
    """Not supported chain error handler."""
    return str(error)


@exceptions_bp.app_errorhandler(HTTPError)
@render_error_page()
def handle_starknet_api_errors(error: HTTPError) -> HTTPError:
    """StarkNet API errors handler."""
    return error


@exceptions_bp.app_errorhandler(Exception)
@render_error_page(status=500)
def handle_all_exceptions(error: Exception) -> str:
    """All Exceptions handler."""
    log.exception(str(error))

    return "Unexpected error"
