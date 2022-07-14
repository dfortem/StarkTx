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

from functools import wraps
from typing import Callable, Dict, Optional, Union, Type

from flask import Blueprint, Flask

from app import factory
from app.engine.providers.semantics import load_semantics


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

        f.__name__ = str(id(f)) + f.__name__
        return f

    return decorator
