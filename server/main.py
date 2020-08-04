from server.game import game
from server.holdRequest import HoldRequest
from server.createApp import create_app
from flask import request, jsonify

# todo home page:

# @app.route("/")
# def homePage():
#     print("homepage")
#     print(request.headers)
#     return "homepage"
#


if __name__ == '__main__':
    app = create_app()
    app.register_blueprint(game)
    app.register_blueprint(HoldRequest)
    app.run()
