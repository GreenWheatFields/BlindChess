from flask import Blueprint, request, abort
from server.serverMethods import *
import chess
import random

game = Blueprint("game", __name__)

approvedPlayers = {}
setupReady = False


# maybe seperate method calls in a switch statement and call them from some type of master method depending on the header
@game.route("/game", methods=["GET", "POST"])
def createGame():
    def gameReady():
        setupReady = True
        return "ready"

    checkSession()
    approvedUser = session['userID'] in approvedPlayers
    global setupReady
    lobbySize = len(approvedPlayers)

    if not setupReady and lobbySize < 2:
        print("here")
        print(lobbySize)
        if not approvedUser:
            approvedPlayers[session['userID']] = None
            print(approvedPlayers)
            return "waiting" if len(approvedPlayers) < 2 else gameReady()
        elif approvedUser:
            return "waiting"
        else:
            gameReady()
    if approvedUser:
        return "ready"
    elif not approvedUser:
        abort(404, "lobby full")


def setupGame():
    board = chess.Board()


# @game.errorhandler(404)
# def lobbyFullError():
#     return "lobby full", 404
