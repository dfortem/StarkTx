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

import logging
from functools import wraps
from typing import Callable, Optional

from flask import Blueprint, render_template
from requests import HTTPError
from werkzeug.exceptions import HTTPException

from app.base_exceptions import NotSupportedChainError, TransactionStatusError
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


@exceptions_bp.app_errorhandler(TransactionStatusError)
@render_error_page(status=404)
def handle_transaction_status_error(error: TransactionStatusError) -> str:
    """Transaction status error handler."""
    return str(error)


@exceptions_bp.app_errorhandler(Exception)
@render_error_page(status=500)
def handle_all_exceptions(error: Exception) -> str:
    """All Exceptions handler."""
    log.exception(str(error))

    return "Unexpected error"
