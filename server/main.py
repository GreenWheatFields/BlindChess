from server.game import game
from tests.holdRequest import HoldRequest
from server.createApp import create_app

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
