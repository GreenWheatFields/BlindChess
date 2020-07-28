from flask import Flask
from server.KEYS import *
from server.game import game
import server
import importlib


def create_app():
    app = Flask(__name__)
    app.secret_key = SECRET_KEY
    #only importing once
    importlib.reload(server.game)
    print("creating app")
    app.register_blueprint(game)
    return app
