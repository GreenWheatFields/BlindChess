import random

import chess
from flask import Blueprint, abort, request, jsonify

from server.serverMethods import *

game = Blueprint("game", __name__)

approvedPlayers = {}
approvedUser = None
setupReady = False
board = None
turn = None


@game.route("/game/", methods=["GET", "POST"])
def handleRequest():
    global setupReady, approvedUser, approvedPlayers
    # parseArguments()
    print(request.method)
    print(approvedUser)
    if not setupReady:
        return createGame()
    elif not approvedUser:
        abort(404, "lobby full")
    else:
        # return playChess(parseArguments())
        return "placeholder"


# def parseArguments():
#     args = request.args
#     # print(args)
#     if "move" in args:
#         return args.get("move")


def createGame():
    def gameReady():
        global setupReady
        setupReady = True
        # TODO: let users pick colors
        return setupGame()

    global setupReady, approvedUser, approvedPlayers
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
    global board, turn
    board = chess.Board()
    approvedPlayers[list(approvedPlayers.keys())[0]] = chess.BLACK if random.randrange(2) + 1 == 2 else chess.WHITE
    approvedPlayers[list(approvedPlayers.keys())[1]] = not approvedPlayers[list(approvedPlayers.keys())[0]]
    turn = False if random.randrange(2) + 1 == 1 else True
    # return jsonify(turn=turn)
    return "placeholder"


def playChess(move: str):
    print(move)
    global board
    pass
