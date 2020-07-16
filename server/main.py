from server import app
from server.game import game

app.register_blueprint(game)

@app.route("/")
def homePage():
    print("homepage")
    return "homepage"

if __name__ == '__main__':
    print("http://127.0.0.1:5000/game")
    app.run()
