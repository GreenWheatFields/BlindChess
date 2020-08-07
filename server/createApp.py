from flask import Flask
from server.game import game
from server.holdRequest import HoldRequest
import server
import importlib
import os
import sys


def create_app():
    app = Flask(__name__)
    if os.getenv("SECRET_KEY") is None:
        raise Exception("NoSecretKey")
    app.secret_key = os.getenv("SECRET_KEY")
    importlib.reload(server.game)
    importlib.reload(server.holdRequest)
    app.register_blueprint(game)
    app.register_blueprint(HoldRequest)
    return app
