from server import app
from server.game import game
from flask import request

app.register_blueprint(game)

@app.route("/")
def homePage():
    print("homepage")
    print(request.headers)
    return "homepage"


if __name__ == '__main__':
    app.run()
