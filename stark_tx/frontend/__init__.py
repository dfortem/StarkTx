from functools import wraps
from typing import Callable, Dict, Optional, Union, Type

from flask import Blueprint, Flask

from .. import factory
from ..engine.providers.semantics import load_semantics


def create_app(settings_override: Optional[Union[Dict, Type]] = None) -> Flask:
    """Returns Frontend app instance."""
    app = factory.create_app(
        __name__,
        __path__,
        settings_override,
        template_folder="frontend/templates",
        static_folder="frontend/static",
    )

    app.jinja_env.trim_blocks = True
    app.jinja_env.lstrip_blocks = True

    load_semantics()

    return app


def frontend_route(bp: Blueprint, *args, **kwargs):
    """Route in blueprint context."""

    def decorator(f: Callable):
        @bp.route(*args, **kwargs)
        @wraps(f)
        def wrapper(*args, **kwargs):
            return f(*args, **kwargs)

        return f

    return decorator
