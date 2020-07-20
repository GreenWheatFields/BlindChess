import random

import chess
from flask import Blueprint, abort, request

from server.serverMethods import *

game = Blueprint("game", __name__)

approvedPlayers = {}
approvedUser = None
setupReady = False
board = None


# maybe seperate method calls in a switch statement and call them from some type of master method depending on the header
@game.route("/game/", methods=["GET", "POST"])
def handleRequest():
    global setupReady, approvedUser
    print(request.args.get("move"))
    if not setupReady:
        return createGame()
    elif not approvedUser:
        abort(404, "lobby full")
    else:
        #todo. method to parse arguments
        return playChess("",None)


def createGame():
    def gameReady():
        global setupReady
        setupReady = True
        # TODO: let users pick colors
        setupGame()
        return "ready"

    global setupReady, approvedUser
    checkSession()
    approvedUser = session['userID'] in approvedPlayers
    lobbySize = len(approvedPlayers)
    if not setupReady and lobbySize < 2:
        if not approvedUser:
            approvedPlayers[session['userID']] = None
            return "waiting" if len(approvedPlayers) < 2 else gameReady()
        elif approvedUser:
            return "waiting"
        else:
            gameReady()
    if approvedUser:
        return "ready"


def setupGame():
    global board
    board = chess.Board()
    approvedPlayers[list(approvedPlayers.keys())[0]] = chess.BLACK if random.randrange(2) + 1 == 2 else chess.WHITE
    approvedPlayers[list(approvedPlayers.keys())[1]] = not approvedPlayers[list(approvedPlayers.keys())[0]]


def playChess(move: str, board: chess.Board()):
    pass
