from flask import Blueprint, render_template

exceptions = Blueprint("exceptions", __name__)


@exceptions.app_errorhandler(404)
def handle_404(*_):
    return render_template("app/templates/404.html"), 404
