from flask import Flask
from server.game import game
import server
import importlib
import os


def create_app():
    app = Flask(__name__)
    app.secret_key = os.getenv("SECRET_KEY")
    importlib.reload(server.game)
    app.register_blueprint(game)
    return app
