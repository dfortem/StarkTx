from flask import Flask
from werkzeug.middleware.dispatcher import DispatcherMiddleware

from stark_tx import frontend

app = Flask(__name__)

app.wsgi_app = DispatcherMiddleware(frontend.create_app())

if __name__ == "__main__":
    app.run()
