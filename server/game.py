from flask import Blueprint, request
from server.serverMethods import *

game = Blueprint("game", __name__)

approvedPlayers = set()


@game.route("/game", methods=["GET", "POST"])
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
