from server import app
from flask import session
from server.serverMethods import *

approvedPlayers = set


@app.route("/game/")
def setUp():
    print(session)
    checkSession()
    approvedPlayers.update(session['userID'])
    print(approvedPlayers)
    print(session)
    return "lol"


if __name__ == '__main__':
    app.run()
