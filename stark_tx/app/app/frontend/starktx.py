from flask import render_template, Blueprint

from app.core.config import settings
from . import frontend_route

bp = Blueprint("static", __name__)


@frontend_route(bp, "/")
def route_home():
    return render_template("index.html", config=settings.SEQUENCERS.items()), 200
