import importlib
import logging
import pkgutil
from typing import Any, List

from flask import Blueprint, Flask

log = logging.getLogger(__name__)


def register_blueprints(
    app: Flask, package_name: str, package_path: str
) -> List[Blueprint]:
    """
    Register all Blueprint instances on the specified Flask application found
    in all modules for the specified package.
    :param app: the Flask application
    :param package_name: the package name
    :param package_path: the package path
    """
    rv = []

    for _, name, _ in pkgutil.iter_modules(package_path):
        m = importlib.import_module("%s.%s" % (package_name, name))
        for item in dir(m):
            item = getattr(m, item)
            if isinstance(item, Blueprint):
                app.register_blueprint(item)
            rv.append(item)

    return rv


def class_import(name: str) -> Any:
    """Import class from string."""
    d = name.rfind(".")
    classname = name[d + 1 : len(name)]
    m = __import__(name[0:d], globals(), locals(), [classname])

    return getattr(m, classname)


class Singleton(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]
