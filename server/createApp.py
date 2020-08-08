from flask import Flask
from server.game import game
import tests
from tests.holdRequest import HoldRequest
import server
import importlib
import os


def create_app(debug=True):
    app = Flask(__name__)
    if os.getenv("SECRET_KEY") is None:
        raise Exception("NoSecretKey")
    app.secret_key = os.getenv("SECRET_KEY")
    importlib.reload(server.game)
    app.register_blueprint(game)
    if debug:
        importlib.reload(tests.holdRequest)
        app.register_blueprint(HoldRequest)
    return app
