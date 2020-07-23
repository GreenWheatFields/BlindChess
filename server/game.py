import random

import chess
from flask import Blueprint, abort, request, jsonify

from server.serverMethods import *

game = Blueprint("game", __name__)

approvedPlayers = {}
approvedUser = None
setupReady = False
board = chess.Board()
turn = None


@game.route("/game/", methods=["GET", "POST"])
def handleRequest():
    global setupReady, approvedUser, approvedPlayers
    # parseArguments()
    checkSession()
    approvedUser = session['userID'] in approvedPlayers
    if not setupReady:
        return createGame()
    elif not approvedUser:
        abort(404, "lobby full")
    else:
        return playChess(request.args.get("move"))


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
    global turn
    approvedPlayers[list(approvedPlayers.keys())[0]] = chess.BLACK if random.randrange(2) + 1 == 2 else chess.WHITE
    approvedPlayers[list(approvedPlayers.keys())[1]] = not approvedPlayers[list(approvedPlayers.keys())[0]]
    turn = chess.WHITE if random.randrange(2) + 1 == 1 else chess.BLACK
    # return jsonify(turn=turn)
    return "placeholder"


def playChess(move: str):
    global board, turn
    print(move)
    x = board.legal_moves
    y = chess.Move.from_uci("g1h3")
    print(board.is_legal(y))
    print(type(x))

    if approvedPlayers.get(session["userID"]) != turn:
        abort(404)

    return "placeholder"
