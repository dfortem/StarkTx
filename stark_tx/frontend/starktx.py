from flask import render_template, Blueprint

from . import frontend_route

bp = Blueprint("statktx", __name__)


@frontend_route(bp, "/")
def route_home():
    return render_template("index.html"), 200
