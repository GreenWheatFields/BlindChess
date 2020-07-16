from flask import Blueprint
from server.serverMethods import *

game = Blueprint("game", __name__)

approvedPlayers = set()
@game.route("/game")
def beginGame():
    checkSession()
    print(session)
    if session['userID'] not in approvedPlayers and len(approvedPlayers) < 2:
        approvedPlayers.add(session['userID'])
    print(session)
    print(approvedPlayers)
    if len(approvedPlayers) < 2:
        return "waiting for player"
    else:
        return "ready"
